#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Python implementation of UCR_DTW & UCR_ED algorithm

ref:

- [code-python] https://github.com/JozeeLin/ucr-suite-python/blob/master/DTW.ipynb
- [code-C] https://github.com/klon/ucrdtw/blob/master/src/ucrdtw.c
- [paper] https://www.cs.ucr.edu/~eamonn/SIGKDD_trillion.pdf

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/10/17 下午2:27
"""

from __future__ import unicode_literals, division, print_function

from collections import Counter

from typing import Sequence, Callable, TypeVar, Iterable, Tuple, Any, Union
import numpy as np
from numpy import ndarray
from functional import seq
from scipy.sparse import dok_matrix
from six.moves import map as map
from six.moves import zip as zip
from six.moves import xrange as range

from sklearn.preprocessing import StandardScaler

from kinoko.func import profile
from kinoko.misc.log_writer import init_log

INF = float('inf')
NAN = np.nan
logger = init_log(__name__, level='DEBUG')


def square_dist_fn(v1, v2):
    return (v1 - v2) ** 2


class MovingStatistics(object):
    def __init__(self, mean=NAN, std=NAN):
        self.cum_x = 0
        self.cum_x2 = 0
        self.n_points = 0

        self.mean = mean
        self.std = std

    def feed(self, x):
        self.cum_x += x
        self.cum_x2 += x ** 2
        self.n_points += 1

    def drop(self, x):
        self.cum_x -= x
        self.cum_x2 -= x ** 2
        self.n_points -= 1

    def mv_mean(self):
        return self.cum_x / self.n_points

    def mv_std(self):
        return np.sqrt(self.cum_x2 / self.n_points - self.mv_mean() ** 2)

    def snapshot(self):
        self.mean = self.mv_mean()
        self.std = self.mv_std()

    def znorm(self, *args):
        # type: (Any) -> Union[float, ndarray]
        if len(args) == 1:
            return (args[0] - self.mean) / self.std
        else:
            return (np.array(args) - self.mean) / self.std


class UCR_DTW(object):
    # reset_period = 5000  # for debug
    reset_period = 100000  # for “flush out” any accumulated floating error

    def __init__(self, dist_cb=square_dist_fn, window_frac=0.05):
        # type: (Callable[[float, float], float], float) -> None
        """
        :param dist_cb: callback function to calculate distance two floats
        :param window_frac: window_size will be calculated by `int(len(query) * window_frac)`
                            read the KDD-paper chapter 3.1 for Sakoe-Chiba-Band related concepts
        """
        self.dist_cb = dist_cb
        self.window_frac = window_frac  # type: float

        # a few internal states for `search()`
        self.buffer = []
        self.loc = None  # type: int
        self.best_so_far = INF

    @profile
    def search(self, content, query, window_frac=None):
        # type: (Iterable[float], Sequence[float], Union[float, None]) -> Tuple[int, float, dict]
        """
        Search `query` in `content`, find its nearest match period;
        returning that period's starting index and DTW_distance and running details

        :param content: a sequence of floats, which can be used to compute distance by `self.dist_cb()`
        :param query: a (typically) shorter sequence than content, which need to be searched for
        :param window_frac: overwrite object variable if needed; see `__init__()` for detail
        :return: tuple of: location, DTW_distance, running_details_as_dict
        """
        Q = len(query)
        self.best_so_far = INF  # reset best cost for a new search
        q_norm = StandardScaler().fit_transform(query[:, None]).flatten()  # z-norm the q

        # create envelops for normalized query (viz. LB_Keogh_EQ)
        window_size = int(Q * (window_frac or self.window_frac))
        q_norm_L, q_norm_U = self._lower_upper_lemire(q_norm, r=window_size)
        q_argidx = q_norm.__abs__().argsort()[::-1]  # decreasing order
        q_norm_dec, q_norm_L_dec, q_norm_U_dec = q_norm[q_argidx], q_norm_L[q_argidx], q_norm_U[q_argidx]

        idx_buf = 0
        done = False
        prune_cnt = Counter(kim=0, eg=0, ec=0)  # pruning counters for each phase
        while not done:
            # use the last `m-1` points if available
            self.buffer = [] if idx_buf == 0 else self.buffer[-(Q - 1):]
            self.buffer += seq(content).take(self.reset_period - len(self.buffer)).to_list()
            # CAUTION: `self.buffer` is huge, DO NOT PUT IT INNER LOOP
            buf_L, buf_U = self._lower_upper_lemire(self.buffer, r=window_size)  # for calc LB_Keogh_EC

            if len(self.buffer) <= Q - 1:
                break

            C_stat = MovingStatistics()  # start calculating online z-norm for points in buffer
            # a circular array for keeping current content region; double size for avoiding "%" operator
            C = np.zeros(Q * 2)  # candidate C sequence

            for idx_p, p in enumerate(self.buffer):
                C_stat.feed(p)
                C[(idx_p % Q) + Q] = C[idx_p % Q] = p
                if idx_p < Q - 1:
                    continue

                C_stat.snapshot()
                i = (idx_p + 1) % Q  # index in C

                # ----- LB_KimFL
                lb_kim = self._lb_kim_hierarchy(C, i, C_stat, q_norm)
                if lb_kim >= self.best_so_far:
                    prune_cnt['kim'] += 1
                    # reduce obsolute points from sum and sum square
                    C_stat.drop(C[i])  # recall: `i = (idx_p + 1) % Q` ; circularly map to the left neighbor
                    continue  # CAUTION: DO NOT FORGET TO `drop` BEFORE `continue`

                # ----- LB_Keogh_EQ
                lb_keogh_eg, cb_eg = self._lb_keogh_online(C_stat, q_argidx, q_norm_L_dec, q_norm_U_dec, C=C[i:])
                if lb_keogh_eg >= self.best_so_far:
                    prune_cnt['eg'] += 1
                    C_stat.drop(C[i])
                    continue

                # ----- LB_Keogh_EC
                idx_in_query = idx_p - (Q - 1)  # start location of the data in `query`
                lb_keogh_ec, cb_ec = self._lb_keogh_online(C_stat, q_argidx,  # CAUTION: keep ordered beforehand
                                                           buf_L[idx_in_query:][q_argidx],
                                                           buf_U[idx_in_query:][q_argidx], q_norm=q_norm)
                if lb_keogh_ec >= self.best_so_far:
                    prune_cnt['ec'] += 1
                    C_stat.drop(C[i])
                    continue

                # ----- DTW
                # backward cumsum cb_eg & cb_ec to use in early abandoning DTW
                cb_backcum = np.cumsum((cb_ec if lb_keogh_ec > lb_keogh_eg else cb_eg)[::-1])[::-1]
                c = self.dtw_distance(C_stat.znorm(C[i:i + Q]), q_norm, max_stray=window_size, cb_backcum=cb_backcum)
                if c < self.best_so_far:
                    self.best_so_far = c
                    self.loc = idx_buf * (self.reset_period - Q + 1) + idx_p - Q + 1
                C_stat.drop(C[i])
                logger.debug((idx_buf, idx_p, c, self.best_so_far))

            # if idx_buf >= 2: # for debug
            #     done = True
            if len(self.buffer) < self.reset_period:
                done = True
            else:
                idx_buf += 1

            logger.info("#################### %d %d ####################", idx_buf, len(self.buffer))

        n_scanned = idx_buf * (self.reset_period - Q + 1) + len(self.buffer)
        result_json = {
            "location": self.loc, "dtw_distance": np.sqrt(self.best_so_far),
            "n_scanned: ": n_scanned, "n_prunes": prune_cnt, "n_calc_dtw": (n_scanned - sum(prune_cnt.values()))
        }
        return self.loc, np.sqrt(self.best_so_far), result_json

    @staticmethod
    def _lower_upper_lemire(s, r):
        # type: (Sequence[float], int) -> Tuple[ndarray, ndarray]
        """
        Finding the envelop of min and max value for LB_Keogh_EQ or EC
        Implementation idea is introducted by Danial Lemire in his paper
        "Faster Retrieval with a Two-Pass Dynamic-Time-Warping Lower Bound",Pattern Recognition 42(9) 2009
        """
        size = len(s)
        L, U = np.empty(size), np.empty(size)
        for j in range(size):  # should replace loop with vectorization for speed
            region = s[max(j - r, 0): min(j + r + 1, size)]  # CAUTION: `r+1` right open
            L[j], U[j] = min(region), max(region)
        return L, U

    def _lb_kim_hierarchy(self, C, i, C_stat, query):
        # type: (ndarray, int, MovingStatistics, Sequence[float]) -> float
        """
        Usually, LB_Kim take time O(m) for finding top,bottom,first and last
        however, because of z-normalization the top and bottom cannot give significant benefits
        and using the first and last points can be computed in constant time
        the prunning power of LB_Kim is non-trivial,especially when the query is not long, say in length 128

        :param C: C un-normed
        :param i: starting index in C
        :param C_stat:
        :param query: query normed
        :return:
        """
        Q = len(query)
        # 1 point at front and back
        x0, y0 = C_stat.znorm(C[i], C[(i + Q - 1)])
        lb = self.dist_cb(x0, query[0]) + self.dist_cb(y0, query[Q - 1])
        if lb >= self.best_so_far:
            return lb

        # 2 points at front
        x1 = C_stat.znorm(C[i + 1])
        lb += min(self.dist_cb(x1, query[0]), self.dist_cb(x0, query[1]), self.dist_cb(x1, query[1]))
        if lb >= self.best_so_far:
            return lb

        # 2 points at back
        y1 = C_stat.znorm(C[(i + Q - 2)])
        lb += min(self.dist_cb(y1, query[Q - 1]), self.dist_cb(y0, query[Q - 2]), self.dist_cb(y1, query[Q - 2]))
        if lb >= self.best_so_far:
            return lb

        # 3 points at front
        x2 = C_stat.znorm(C[(i + 2)])
        lb += min(self.dist_cb(x0, query[2]), self.dist_cb(x1, query[2]),
                  self.dist_cb(x2, query[2]), self.dist_cb(x2, query[1]), self.dist_cb(x2, query[0]))
        if lb >= self.best_so_far:
            return lb

        # 3 points at back
        y2 = C_stat.znorm(C[(i + Q - 3)])
        lb += min(self.dist_cb(y0, query[Q - 3]), self.dist_cb(y1, query[Q - 3]),
                  self.dist_cb(y2, query[Q - 3]), self.dist_cb(y2, query[Q - 2]), self.dist_cb(y2, query[Q - 1]))
        return lb

    @profile
    def _lb_keogh_online(self, C_stat, q_argidx, L, U, C=None, q_norm=None):
        # type: (MovingStatistics, ndarray, ndarray, ndarray, ndarray, ndarray) -> Tuple[float, ndarray]
        """
        LB_Keogh for EG/EC : Create Envelop for the query or data

        :param C_stat: statistical info of C
        :param q_argidx: pseudo-code: map(abs, query).argidx().reverse()
        :param L: for "LB_keogh_EG" case, `L` means neighbor_lower_bound for normalized `query`
                  for "...EC" case, means ... for `buffer` region, un-normed, but reordered by q_argidx
        :param U: ... upper ...
        :param C: needed in "EG" case
        :param q_norm: needed in "EC" case
        :return: a tuple of: lowest_bound, current_bound_for_each_position
        """
        assert not (C is None and q_norm is None), 'C and q_norm should not be None together'
        lb = 0.0
        Q = len(U)
        cb = np.zeros(Q)

        for i, l, u in zip(q_argidx, L, U):
            if lb >= self.best_so_far:
                break

            if C is not None:  # EG case
                x = C_stat.znorm(C[i])  # elements of C need to be normed "on the fly"
                # `u, l` of query (in EG case) are already normed
            else:
                x = q_norm[i]
                # noinspection PyPep8
                u, l = C_stat.znorm(u, l)

            if x > u:
                d = self.dist_cb(x, u)
            elif x < l:
                d = self.dist_cb(x, l)
            else:
                d = 0
            lb += d
            cb[i] = d  # for usage in Early Abandoning of DTW
        return lb, cb

    @profile
    def dtw_distance(self, content, query, max_stray=None, cb_backcum=None, rolling_level=2):
        # type: (Sequence[float], Sequence[float], int, ndarray, int) -> float
        """
        calculate the DTW distance between two sequences: `content` & `query`

        :param content: to which compare against
        :param query: to which compare for
        :param max_stray: how many cells should not the warping path deviate beyond. c.f. Sakoe-Chiba Band
                          default use a tight value: abs(len(C)-len(Q))
        :param cb_backcum: current_lower_bound which is cumsum'ed backward;
                           approximates the lower bound of `dtw_cost(current_position -> north_east_corner)`.
                           qv. Figure 6, right subplot in the KDD paper.
        :param rolling_level: level of DP rolling trick for memory-optimization
        :return: DTW distance
        """
        C, Q = len(content), len(query)
        assert C > 0, 'Empty content to compare against'
        assert Q > 0, 'Empty query to compare for'
        if max_stray is None:
            max_stray = abs(C - Q)  # default
        assert 0 <= max_stray <= min(C, Q) - 1, 'invalid max_stray'
        if cb_backcum is not None:
            assert len(content) == len(query), 'len(content) != len(query), `cb` should be None'

        def early_abandon_by_cb_backcum(i, mc):  # inner function to save arguments
            """
            Consider a "higher"(northern) point, say `(x, y)` where x > i;
            whose DP path cost consists of two parts:

            1. `(0,0) --> (x,y)`
            2. `(x,y) --> (C-1,Q-1)`

            For the first part, define `min_cost(x)` as `min(dp[x,:])`.
            Since cost is mono-increasing w.r.t. row index, and `x > i`;
            we known that `min_cost(x) >= min_cost(i)`

            For the second part, just use `cb_backcum` as a lower bound, read Figure 6 in KDD paper for detail.
            we deduce that cost of `(x,y) --> (C-1,Q-1)` >= cb_backcum[x]

            Put it together, we conclude that:
               cost( (0,0) -> (x,y) -> (C-1, Q-1) )
            =  cost( (0,0) -> (x,y) )                  +   cost( (x,y) -> (C-1, Q-1) )
            >= min(dp[x,:])                            +   cb_backcum(x)
            >= min(dp[i,:])                            +   cb_backcum(x)
            """
            x = i + max_stray + 1  # take `x` as large as possibly allowed, for "earlier" abandon
            if cb_backcum is not None and x < C and mc + cb_backcum[x] >= self.best_so_far:
                return mc + cb_backcum[x]
            else:
                return None

        if rolling_level == 0:  # naive version, for easy understanding; O(C*Q) space
            # dp[i, j] defined as: DTW_distance between content[:i+1] & query[:j+1], excluding right bound
            dp = dok_matrix((C, Q), dtype=float)
            for i in range(C):
                mc = INF  # ignore for now; means the `min(dp[i,:])` concept as pseudo code below

                for j in range(Q):
                    if abs(j - i) > max_stray:
                        dp[i, j] = INF
                        continue
                    if i == j == 0:  # can not go back beyond 0
                        base = 0
                    elif i == 0:
                        base = dp[i, j - 1]
                    elif j == 0:
                        base = dp[i - 1, j]
                    else:
                        base = min(dp[i - 1, j], dp[i, j - 1], dp[i - 1, j - 1])
                    dp[i, j] = base + self.dist_cb(content[i], query[j])
                    mc = min(mc, dp[i, j])

                r = early_abandon_by_cb_backcum(i, mc)
                if r is not None:
                    return r
            return dp[-1, -1]

        elif rolling_level == 1:  # O(Q) space
            # rolling DP now defined as: current row of DTW distance
            dp = np.cumsum([self.dist_cb(content[0], q) if j <= max_stray else INF
                            for j, q in enumerate(query)])
            for i in range(1, C):  # starting from the second row, and goes north
                mc = INF  # see above `rolling_level == 0` case
                for j in range(Q):  # going east
                    if not i - max_stray <= j <= i + max_stray:
                        # keep current state of `dp[j]` as south_west for next j
                        south_west = dp[j]  # CAUTION: before modification by current j: `dp[j] = INF`
                        dp[j] = INF
                        continue

                    if j == 0:  # there is no west or south_west for the head
                        base = dp[j]
                    else:
                        # noinspection PyUnboundLocalVariable
                        base = min(dp[j - 1], south_west, dp[j])  # base comes from: min(west, south_west, south)
                    # CAUTION:
                    # - after usage (see above): `... = min(..., south_west, ...)`
                    # - before modification (see below): `dp[j] = base + ...`
                    south_west = dp[j]
                    dp[j] = base + self.dist_cb(content[i], query[j])  # we can modify it now, after keeping
                    mc = min(mc, dp[j])

                r = early_abandon_by_cb_backcum(i, mc)
                if r is not None:
                    return r
            return dp[-1]

        elif rolling_level == 2:  # O(max_stray) space
            # when calculating cell (i,j), we only need last row's cache of `[i-1, j-max_stray: j+max_stray+1]`
            # thus, achieving O(max_stray) space
            # IT IS NOT REALLY INTUITIVE; PLEASE READ C-CODE BELOW FOR DETAIL
            # https://github.com/klon/ucrdtw/blob/afc6ff0ac83746378da8cc493bfb09f259f988ee/src/ucrdtw.c#L281
            cost = [INF] * (2 * max_stray + 1)
            cost_prev = [INF] * (2 * max_stray + 1)
            for i in range(C):
                k = max(0, max_stray - i)
                mc = INF

                for j in range(max(0, i - max_stray), min(Q, i + max_stray + 1)):
                    if i == j == 0:
                        base = 0
                    else:
                        u = INF if i < 1 or k + 1 > 2 * max_stray else cost_prev[k + 1]
                        v = INF if j < 1 or k < 1 else cost[k - 1]
                        w = INF if i < 1 or j < 1 else cost_prev[k]
                        base = min(u, v, w)
                    cost[k] = base + self.dist_cb(content[i], query[j])
                    if cost[k] < mc:
                        mc = cost[k]
                    k += 1

                r = early_abandon_by_cb_backcum(i, mc)
                if r is not None:
                    return r
                cost, cost_prev = cost_prev, cost
            k -= 1
            return cost_prev[k]

        else:
            raise ValueError('invalid value for rolling_level: {}'.format(rolling_level))


def _demo_entry():
    model = UCR_DTW()
    model.search(content=map(eval, open('data/Data_new.txt')), query=np.loadtxt('data/Query_new.txt'))

# if __name__ == '__main__':
#     _demo_entry()
