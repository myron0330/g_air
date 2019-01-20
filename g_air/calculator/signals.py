"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: signals calculating file.
#   Author: Myron
# **********************************************************************************#
"""
import numpy as np
import pandas as pd
from .factors import *


def calculate_signal_m(q_series=None, m_series=None, **cal_args):
    """
    Calculate signal Ms(n).

    2.1) Ms(n) = Q(n) + M(n)

    Args:
        q_series(Series): Q(n) series.
        m_series(Series): M(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal Ms(n) series.
    """
    if q_series is None:
        q_series = calculate_factor_q(**cal_args)
    if m_series is None:
        m_series = calculate_factor_m(**cal_args)
    return q_series + m_series


def calculate_signal_w(m_series=None, w_series=None, **cal_args):
    """
    Calculate signal Ws(n).

    2.2) Ws(n) = M(n) + W(n)

    Args:
        m_series(Series): M(n) series.
        w_series(Series): W(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal Ws(n) series.
    """
    if m_series is None:
        m_series = calculate_factor_m(**cal_args)
    if w_series is None:
        w_series = calculate_factor_w(**cal_args)
    return m_series + w_series


def calculate_signal_d(w_series=None, d_series=None, **cal_args):
    """
    Calculate signal Ds(n).

    2.3) Ds(n) = W(n) + D(n)

    Args:
        w_series(Series): W(n) series.
        d_series(Series): D(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal Ds(n) series.
    """
    if w_series is None:
        w_series = calculate_factor_w(**cal_args)
    if d_series is None:
        d_series = calculate_factor_d(**cal_args)
    return w_series + d_series


def calculate_signal_m1(ms_series=None, **cal_args):
    """
    Calculate signal M1(n)

    3.1)        Ms(n) > 5 --> -3;   4 < Ms(n) <= 5 --> -2;   3 < Ms(n) <= 4 --> -1;
                Ms(n) <= -9 --> 5;   -9 < Ms(n) <= -8 --> 4;  -8 < Ms(n) <= -7 --> 3;
                -7 < Ms(n) <= -6 --> 2;  -6 < Ms(n) <= -5 --> 1

                else: 0

    Args:
        ms_series(Series): signal Ms(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal M1(n) series.
    """

    def _grade(signal):
        """
        Grade a specific signal value.

        Args:
            signal: signal value.

        Returns:
            int: score of signal deserved.
        """
        score = 0
        if signal > 5:
            score = -3
        if 4 < signal <= 5:
            score = -2
        if 3 < signal <= 4:
            score = -1
        if signal <= -9:
            score = 5
        if -9 < signal <= -8:
            score = 4
        if -8 < signal <= -7:
            score = 3
        if -7 < signal <= -6:
            score = 2
        if -6 < signal <= -5:
            score = 1
        return score

    if ms_series is None:
        ms_series = calculate_signal_m(**cal_args)
    return ms_series.apply(_grade)


def calculate_signal_m2(ms_series=None, ms_series_offset_20=None, **cal_args):
    """
    Calculate signal M2(n).

    3.2)        Ms(n) > Ms(n-20) --> 1;       Ms(n) < Ms(n-20) --> -1;      Ms(n) == Ms(n-20) --> 0

    Args:
        ms_series(Series): signal Ms(n) series.
        ms_series_offset_20(Series): signal Ms(n-20) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal M2(n) series.
    """
    if ms_series is None:
        ms_series = calculate_signal_m(**cal_args)
    if ms_series_offset_20 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 20
        ms_series_offset_20 = calculate_signal_m(**cal_args)
    return (ms_series - ms_series_offset_20).apply(np.sign)


def calculate_signal_m3(c_series=None, c_series_offset_20=None, **cal_args):
    """
    Calculate signal M3(n).

    3.3)        Close(n) > Close(n-20) --> 1;       Close(n) < Close(n-20) --> -1;      Close(n) == Close(n-20) --> 0

    Args:
        c_series(Series): factor Close(n) series.
        c_series_offset_20(Series): factor Close(n-20) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal M3(n) series.
    """
    if c_series is None:
        c_series = get_close_price_series(**cal_args)
    if c_series_offset_20 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 20
        c_series_offset_20 = get_close_price_series(**cal_args)
    return (c_series - c_series_offset_20).apply(np.sign)


def calculate_signal_m4(m_series=None, m_series_offset_20=None, **cal_args):
    """
    Calculate signal M4(n).

    3.4)        M(n) > M(n-20) --> 1;       M(n) < M(n-20) --> -1;      M(n) == M(n-20) --> 0

    Args:
        m_series(Series): factor M(n) series.
        m_series_offset_20(Series): factor M(n-20) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal M4(n) series.
    """
    if m_series is None:
        m_series = calculate_factor_m(**cal_args)
    if m_series_offset_20 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 20
        m_series_offset_20 = calculate_factor_m(**cal_args)
    return (m_series - m_series_offset_20).apply(np.sign)


def calculate_signal_w1(ws_series=None, **cal_args):
    """
    Calculate signal W1(n)

    3.1)        Ws(n) > 5 --> -3;   4 < Ws(n) <= 5 --> -2;   3 < Ws(n) <= 4 --> -1;
                Ws(n) <= -9 --> 5;   -9 < Ws(n) <= -8 --> 4;  -8 < Ws(n) <= -7 --> 3;
                -7 < Ws(n) <= -6 --> 2;  -6 < Ws(n) <= -5 --> 1

                else: 0

    Args:
        ws_series(Series): signal Ws(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal W1(n) series.
    """

    def _grade(signal):
        """
        Grade a specific signal value.

        Args:
            signal: signal value.

        Returns:
            int: score of signal deserved.
        """
        score = 0
        if signal > 5:
            score = -3
        if 4 < signal <= 5:
            score = -2
        if 3 < signal <= 4:
            score = -1
        if signal <= -9:
            score = 5
        if -9 < signal <= -8:
            score = 4
        if -8 < signal <= -7:
            score = 3
        if -7 < signal <= -6:
            score = 2
        if -6 < signal <= -5:
            score = 1
        return score

    if ws_series is None:
        ws_series = calculate_signal_w(**cal_args)
    return ws_series.apply(_grade)


def calculate_signal_w2(ws_series=None, ws_series_offset_5=None, **cal_args):
    """
    Calculate signal W2(n).

    3.2)        Ws(n) > Ws(n-5) --> 1;       Ws(n) < Ws(n-5) --> -1;      Ws(n) == Ws(n-5) --> 0

    Args:
        ws_series(Series): signal Ws(n) series.
        ws_series_offset_5(Series): signal Ws(n-5) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal W2(n) series.
    """
    if ws_series is None:
        ws_series = calculate_signal_w(**cal_args)
    if ws_series_offset_5 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 5
        ws_series_offset_5 = calculate_signal_w(**cal_args)
    return (ws_series - ws_series_offset_5).apply(np.sign)


def calculate_signal_w3(c_series=None, c_series_offset_5=None, **cal_args):
    """
    Calculate signal W3(n).

    3.3)        Close(n) > Close(n-5) --> 1;       Close(n) < Close(n-5) --> -1;      Close(n) == Close(n-5) --> 0

    Args:
        c_series(Series): factor Close(n) series.
        c_series_offset_5(Series): factor Close(n-5) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal W3(n) series.
    """
    if c_series is None:
        c_series = get_close_price_series(**cal_args)
    if c_series_offset_5 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 5
        c_series_offset_5 = get_close_price_series(**cal_args)
    return (c_series - c_series_offset_5).apply(np.sign)


def calculate_signal_w4(w_series=None, w_series_offset_5=None, **cal_args):
    """
    Calculate signal W4(n).

    3.4)        W(n) > W(n-5) --> 1;       W(n) < W(n-5) --> -1;      W(n) == W(n-5) --> 0

    Args:
        w_series(Series): factor W(n) series.
        w_series_offset_5(Series): factor W(n-5) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal W4(n) series.
    """
    if w_series is None:
        w_series = calculate_factor_w(**cal_args)
    if w_series_offset_5 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 5
        w_series_offset_5 = calculate_factor_w(**cal_args)
    return (w_series - w_series_offset_5).apply(np.sign)


def calculate_signal_d1(ds_series=None, **cal_args):
    """
    Calculate signal D1(n)

    3.1)        Ds(n) > 5 --> -3;   4 < Ds(n) <= 5 --> -2;   3 < Ds(n) <= 4 --> -1;
                Ds(n) <= -9 --> 5;   -9 < Ds(n) <= -8 --> 4;  -8 < Ds(n) <= -7 --> 3;
                -7 < Ds(n) <= -6 --> 2;  -6 < Ds(n) <= -5 --> 1

                else: 0

    Args:
        ds_series(Series): signal Ds(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal D1(n) series.
    """

    def _grade(signal):
        """
        Grade a specific signal value.

        Args:
            signal: signal value.

        Returns:
            int: score of signal deserved.
        """
        score = 0
        if signal > 5:
            score = -3
        if 4 < signal <= 5:
            score = -2
        if 3 < signal <= 4:
            score = -1
        if signal <= -9:
            score = 5
        if -9 < signal <= -8:
            score = 4
        if -8 < signal <= -7:
            score = 3
        if -7 < signal <= -6:
            score = 2
        if -6 < signal <= -5:
            score = 1
        return score

    if ds_series is None:
        ds_series = calculate_signal_d(**cal_args)
    return ds_series.apply(_grade)


def calculate_signal_d2(ds_series=None, ds_series_offset_1=None, **cal_args):
    """
    Calculate signal D2(n).

    3.2)        Ds(n) > Ds(n-1) --> 1;       Ds(n) < Ds(n-1) --> -1;      Ds(n) == Ds(n-1) --> 0

    Args:
        ds_series(Series): signal Ds(n) series.
        ds_series_offset_1(Series): signal Ds(n-1) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal D2(n) series.
    """
    if ds_series is None:
        ds_series = calculate_signal_d(**cal_args)
    if ds_series_offset_1 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 1
        ds_series_offset_1 = calculate_signal_d(**cal_args)
    return (ds_series - ds_series_offset_1).apply(np.sign)


def calculate_signal_d3(c_series=None, c_series_offset_1=None, **cal_args):
    """
    Calculate signal D3(n).

    3.3)        Close(n) > Close(n-1) --> 1;       Close(n) < Close(n-1) --> -1;      Close(n) == Close(n-1) --> 0

    Args:
        c_series(Series): factor Close(n) series.
        c_series_offset_1(Series): factor Close(n-1) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal D3(n) series.
    """
    if c_series is None:
        c_series = get_close_price_series(**cal_args)
    if c_series_offset_1 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 1
        c_series_offset_1 = get_close_price_series(**cal_args)
    return (c_series - c_series_offset_1).apply(np.sign)


def calculate_signal_d4(d_series=None, d_series_offset_1=None, **cal_args):
    """
    Calculate signal D4(n).

    3.4)        D(n) > D(n-1) --> 1;       D(n) < D(n-1) --> -1;      D(n) == D(n-1) --> 0

    Args:
        d_series(Series): factor D(n) series.
        d_series_offset_1(Series): factor D(n-1) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal D4(n) series.
    """
    if d_series is None:
        d_series = calculate_factor_d(**cal_args)
    if d_series_offset_1 is None:
        cal_args['offset'] = cal_args.get('offset', 0) - 1
        d_series_offset_1 = calculate_factor_d(**cal_args)
    return (d_series - d_series_offset_1).apply(np.sign)


def calculate_signal_j(m1_series=None, w1_series=None, d1_series=None, **cal_args):
    """
    Calculate signal J(n).

    J(n) = 0.25 * M1(n) + 0.5 * W1(n) + D1(n)

    Args:
        m1_series(Series): signal M1(n) series.
        w1_series(Series): signal W1(n) series.
        d1_series(Series): signal D1(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal J(n) series.
    """
    if m1_series is None:
        m1_series = calculate_signal_m1(**cal_args)
    if w1_series is None:
        w1_series = calculate_signal_w1(**cal_args)
    if d1_series is None:
        d1_series = calculate_signal_d1(**cal_args)
    return 0.25 * m1_series + 0.5 * w1_series + d1_series


def calculate_signal_m2l(m2_series=None, m2_series_offset_1=None, m2_series_offset_2=None,
                         m2_series_offset_3=None, m2_series_offset_4=None, **cal_args):
    """
    Calculate signal M2L(n).

    M2L(n) = M2(n) + M2(n-1) + M2(n-2) + M2(n-3) + M2(n-4)

    Args:
        m2_series(Series): signal M2(n) series.
        m2_series_offset_1(Series): signal M2(n-1) series.
        m2_series_offset_2(Series): signal M2(n-2) series.
        m2_series_offset_3(Series): signal M2(n-3) series.
        m2_series_offset_4(Series): signal M2(n-4) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal M2L(n) series.
    """
    origin_offset = cal_args.get('offset', 0)
    if m2_series is None:
        m2_series = calculate_signal_m2(**cal_args)
    if m2_series_offset_1 is None:
        cal_args['offset'] = origin_offset - 1
        m2_series_offset_1 = calculate_signal_m2(**cal_args)
    if m2_series_offset_2 is None:
        cal_args['offset'] = origin_offset - 2
        m2_series_offset_2 = calculate_signal_m2(**cal_args)
    if m2_series_offset_3 is None:
        cal_args['offset'] = origin_offset - 3
        m2_series_offset_3 = calculate_signal_m2(**cal_args)
    if m2_series_offset_4 is None:
        cal_args['offset'] = origin_offset - 4
        m2_series_offset_4 = calculate_signal_m2(**cal_args)
    return m2_series + m2_series_offset_1 + m2_series_offset_2 + m2_series_offset_3 + m2_series_offset_4


def calculate_signal_w2l(w2_series=None, w2_series_offset_1=None, w2_series_offset_2=None,
                         w2_series_offset_3=None, w2_series_offset_4=None, **cal_args):
    """
    Calculate signal W2L(n).

    W2L(n) = W2(n) + W2(n-1) + W2(n-2) + W2(n-3) + W2(n-4)

    Args:
        w2_series(Series): signal W2(n) series.
        w2_series_offset_1(Series): signal W2(n-1) series.
        w2_series_offset_2(Series): signal W2(n-2) series.
        w2_series_offset_3(Series): signal W2(n-3) series.
        w2_series_offset_4(Series): signal W2(n-4) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal W2L(n) series.
    """
    origin_offset = cal_args.get('offset', 0)
    if w2_series is None:
        w2_series = calculate_signal_w2(**cal_args)
    if w2_series_offset_1 is None:
        cal_args['offset'] = origin_offset - 1
        w2_series_offset_1 = calculate_signal_w2(**cal_args)
    if w2_series_offset_2 is None:
        cal_args['offset'] = origin_offset - 2
        w2_series_offset_2 = calculate_signal_w2(**cal_args)
    if w2_series_offset_3 is None:
        cal_args['offset'] = origin_offset - 3
        w2_series_offset_3 = calculate_signal_w2(**cal_args)
    if w2_series_offset_4 is None:
        cal_args['offset'] = origin_offset - 4
        w2_series_offset_4 = calculate_signal_w2(**cal_args)
    return w2_series + w2_series_offset_1 + w2_series_offset_2 + w2_series_offset_3 + w2_series_offset_4


def calculate_signal_d2l(d2_series=None, d2_series_offset_1=None, d2_series_offset_2=None,
                         d2_series_offset_3=None, d2_series_offset_4=None, **cal_args):
    """
    Calculate signal D2L(n).

    D2L(n) = D2(n) + D2(n-1) + D2(n-2) + D2(n-3) + D2(n-4)

    Args:
        d2_series(Series): signal D2(n) series.
        d2_series_offset_1(Series): signal D2(n-1) series.
        d2_series_offset_2(Series): signal D2(n-2) series.
        d2_series_offset_3(Series): signal D2(n-3) series.
        d2_series_offset_4(Series): signal D2(n-4) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal D2L(n) series.
    """
    origin_offset = cal_args.get('offset', 0)
    if d2_series is None:
        d2_series = calculate_signal_d2(**cal_args)
    if d2_series_offset_1 is None:
        cal_args['offset'] = origin_offset - 1
        d2_series_offset_1 = calculate_signal_d2(**cal_args)
    if d2_series_offset_2 is None:
        cal_args['offset'] = origin_offset - 2
        d2_series_offset_2 = calculate_signal_d2(**cal_args)
    if d2_series_offset_3 is None:
        cal_args['offset'] = origin_offset - 3
        d2_series_offset_3 = calculate_signal_d2(**cal_args)
    if d2_series_offset_4 is None:
        cal_args['offset'] = origin_offset - 4
        d2_series_offset_4 = calculate_signal_d2(**cal_args)
    return d2_series + d2_series_offset_1 + d2_series_offset_2 + d2_series_offset_3 + d2_series_offset_4


def calculate_signal_m4l(m4_series=None, m4_series_offset_1=None, m4_series_offset_2=None,
                         m4_series_offset_3=None, m4_series_offset_4=None, **cal_args):
    """
    Calculate signal M4L(n).

    M4L(n) = M4(n) + M4(n-1) + M4(n-2) + M4(n-3) + M4(n-4)

    Args:
        m4_series(Series): signal M4(n) series.
        m4_series_offset_1(Series): signal M4(n-1) series.
        m4_series_offset_2(Series): signal M4(n-2) series.
        m4_series_offset_3(Series): signal M4(n-3) series.
        m4_series_offset_4(Series): signal M4(n-4) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal M4L(n) series.
    """
    origin_offset = cal_args.get('offset', 0)
    if m4_series is None:
        m4_series = calculate_signal_m4(**cal_args)
    if m4_series_offset_1 is None:
        cal_args['offset'] = origin_offset - 1
        m4_series_offset_1 = calculate_signal_m4(**cal_args)
    if m4_series_offset_2 is None:
        cal_args['offset'] = origin_offset - 2
        m4_series_offset_2 = calculate_signal_m4(**cal_args)
    if m4_series_offset_3 is None:
        cal_args['offset'] = origin_offset - 3
        m4_series_offset_3 = calculate_signal_m4(**cal_args)
    if m4_series_offset_4 is None:
        cal_args['offset'] = origin_offset - 4
        m4_series_offset_4 = calculate_signal_m4(**cal_args)
    return m4_series + m4_series_offset_1 + m4_series_offset_2 + m4_series_offset_3 + m4_series_offset_4


def calculate_signal_w4l(w4_series=None, w4_series_offset_1=None, w4_series_offset_2=None,
                         w4_series_offset_3=None, w4_series_offset_4=None, **cal_args):
    """
    Calculate signal W4L(n).

    W4L(n) = W4(n) + W4(n-1) + W4(n-2) + W4(n-3) + W4(n-4)

    Args:
        w4_series(Series): signal W4(n) series.
        w4_series_offset_1(Series): signal W4(n-1) series.
        w4_series_offset_2(Series): signal W4(n-2) series.
        w4_series_offset_3(Series): signal W4(n-3) series.
        w4_series_offset_4(Series): signal W4(n-4) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal W4L(n) series.
    """
    origin_offset = cal_args.get('offset', 0)
    if w4_series is None:
        w4_series = calculate_signal_w4(**cal_args)
    if w4_series_offset_1 is None:
        cal_args['offset'] = origin_offset - 1
        w4_series_offset_1 = calculate_signal_w4(**cal_args)
    if w4_series_offset_2 is None:
        cal_args['offset'] = origin_offset - 2
        w4_series_offset_2 = calculate_signal_w4(**cal_args)
    if w4_series_offset_3 is None:
        cal_args['offset'] = origin_offset - 3
        w4_series_offset_3 = calculate_signal_w4(**cal_args)
    if w4_series_offset_4 is None:
        cal_args['offset'] = origin_offset - 4
        w4_series_offset_4 = calculate_signal_w4(**cal_args)
    return w4_series + w4_series_offset_1 + w4_series_offset_2 + w4_series_offset_3 + w4_series_offset_4


def calculate_signal_d4l(d4_series=None, d4_series_offset_1=None, d4_series_offset_2=None,
                         d4_series_offset_3=None, d4_series_offset_4=None, **cal_args):
    """
    Calculate signal D4L(n).

    D4L(n) = D4(n) + D4(n-1) + D4(n-2) + D4(n-3) + D4(n-4)

    Args:
        d4_series(Series): signal D4(n) series.
        d4_series_offset_1(Series): signal D4(n-1) series.
        d4_series_offset_2(Series): signal D4(n-2) series.
        d4_series_offset_3(Series): signal D4(n-3) series.
        d4_series_offset_4(Series): signal D4(n-4) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal D4L(n) series.
    """
    origin_offset = cal_args.get('offset', 0)
    if d4_series is None:
        d4_series = calculate_signal_d4(**cal_args)
    if d4_series_offset_1 is None:
        cal_args['offset'] = origin_offset - 1
        d4_series_offset_1 = calculate_signal_d4(**cal_args)
    if d4_series_offset_2 is None:
        cal_args['offset'] = origin_offset - 2
        d4_series_offset_2 = calculate_signal_d4(**cal_args)
    if d4_series_offset_3 is None:
        cal_args['offset'] = origin_offset - 3
        d4_series_offset_3 = calculate_signal_d4(**cal_args)
    if d4_series_offset_4 is None:
        cal_args['offset'] = origin_offset - 4
        d4_series_offset_4 = calculate_signal_d4(**cal_args)
    return d4_series + d4_series_offset_1 + d4_series_offset_2 + d4_series_offset_3 + d4_series_offset_4


def calculate_signal_m2b(m2_series=None, m3_series=None, **cal_args):
    """
    Calculate signal M2B(n).

    M2(n) = M3(n) --> 0;    else --> M2(n)

    Args:
        m2_series(Series): signal M2(n) series.
        m3_series(Series): signal M3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal M2B(n) series.
    """
    if m2_series is None:
        m2_series = calculate_signal_m2(**cal_args)
    if m3_series is None:
        m3_series = calculate_signal_m3(**cal_args)
    multiplier = pd.Series(m2_series == m3_series).apply(lambda x: 0 if x else 1)
    return (m2_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_w2b(w2_series=None, w3_series=None, **cal_args):
    """
    Calculate signal W2B(n).

    W2(n) = W3(n) --> 0;    else --> W2(n)

    Args:
        w2_series(Series): signal W2(n) series.
        w3_series(Series): signal W3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal W2B(n) series.
    """
    if w2_series is None:
        w2_series = calculate_signal_w2(**cal_args)
    if w3_series is None:
        w3_series = calculate_signal_w3(**cal_args)
    multiplier = pd.Series(w2_series == w3_series).apply(lambda x: 0 if x else 1)
    return (w2_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_d2b(d2_series=None, d3_series=None, **cal_args):
    """
    Calculate signal D2B(n).

    D2(n) = D3(n) --> 0;    else --> D2(n)

    Args:
        d2_series(Series): signal D2(n) series.
        d3_series(Series): signal D3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal D2B(n) series.
    """
    if d2_series is None:
        d2_series = calculate_signal_d2(**cal_args)
    if d3_series is None:
        d3_series = calculate_signal_d3(**cal_args)
    multiplier = pd.Series(d2_series == d3_series).apply(lambda x: 0 if x else 1)
    return (d2_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_m4b(m4_series=None, m3_series=None, **cal_args):
    """
    Calculate signal M2B(n).

    M4(n) = M3(n) --> 0;    else --> M4(n)

    Args:
        m4_series(Series): signal M4(n) series.
        m3_series(Series): signal M3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal M4B(n) series.
    """
    if m4_series is None:
        m4_series = calculate_signal_m4(**cal_args)
    if m3_series is None:
        m3_series = calculate_signal_m3(**cal_args)
    multiplier = pd.Series(m4_series == m3_series).apply(lambda x: 0 if x else 1)
    return (m4_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_w4b(w4_series=None, w3_series=None, **cal_args):
    """
    Calculate signal W4B(n).

    W4(n) = W3(n) --> 0;    else --> W4(n)

    Args:
        w4_series(Series): signal W4(n) series.
        w3_series(Series): signal W3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal W4B(n) series.
    """
    if w4_series is None:
        w4_series = calculate_signal_w4(**cal_args)
    if w3_series is None:
        w3_series = calculate_signal_w3(**cal_args)
    multiplier = pd.Series(w4_series == w3_series).apply(lambda x: 0 if x else 1)
    return (w4_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_d4b(d4_series=None, d3_series=None, **cal_args):
    """
    Calculate signal D4B(n).

    D4(n) = D3(n) --> 0;    else --> D4(n)

    Args:
        d4_series(Series): signal D4(n) series.
        d3_series(Series): signal D3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal D2B(n) series.
    """
    if d4_series is None:
        d4_series = calculate_signal_d4(**cal_args)
    if d3_series is None:
        d3_series = calculate_signal_d3(**cal_args)
    multiplier = pd.Series(d4_series == d3_series).apply(lambda x: 0 if x else 1)
    return (d4_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_z(m2l_series=None, m3_series=None,  **cal_args):
    """
    Calculate signal Z(n).

    M2L(n) < 0 & M3(n) = 1 --> M2L(n);    else --> 0

    Args:
        m2l_series(Series): signal M2L(n) series.
        m3_series(Series): signal M3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal Z(n) series.
    """
    if m2l_series is None:
        m2l_series = calculate_signal_m2l(**cal_args)
    if m3_series is None:
        m3_series = calculate_signal_m3(**cal_args)
    multiplier = pd.Series((m2l_series < 0) & (m3_series == 1)).apply(lambda x: 1 if x else 0)
    return (m2l_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_wz(w2l_series=None, w3_series=None,  **cal_args):
    """
    Calculate signal WZ(n).

    W2L(n) < 0 & W3(n) = 1 --> W2L(n);    else --> 0

    Args:
        w2l_series(Series): signal W2L(n) series.
        w3_series(Series): signal W3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal WZ(n) series.
    """
    if w2l_series is None:
        w2l_series = calculate_signal_w2l(**cal_args)
    if w3_series is None:
        w3_series = calculate_signal_w3(**cal_args)
    multiplier = pd.Series((w2l_series < 0) & (w3_series == 1)).apply(lambda x: 1 if x else 0)
    return (w2l_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_t(m2l_series=None, m3_series=None,  **cal_args):
    """
    Calculate signal T(n).

    M2L(n) > 0 & M3(n) = -1 --> M2L(n);    else --> 0

    Args:
        m2l_series(Series): signal M2L(n) series.
        m3_series(Series): signal M3(n) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal T(n) series.
    """
    if m2l_series is None:
        m2l_series = calculate_signal_m2l(**cal_args)
    if m3_series is None:
        m3_series = calculate_signal_m3(**cal_args)
    multiplier = pd.Series((m2l_series > 0) & (m3_series == -1)).apply(lambda x: 1 if x else 0)
    return (m2l_series * multiplier).apply(lambda x: 0 if x == -0 else x)


def calculate_signal_zq(j_series=None, j_series_offset_1=None, j_series_offset_2=None,
                        j_series_offset_3=None, j_series_offset_4=None, **cal_args):
    """
    Calculate signal ZQ(n).

    ZQ(n) = J(n) + J(n-1) + J(n-2) + J(n-3) + J(n-4)

    Args:
        j_series(Series): signal J(n) series.
        j_series_offset_1(Series): signal J(n-1) series.
        j_series_offset_2(Series): signal J(n-2) series.
        j_series_offset_3(Series): signal J(n-3) series.
        j_series_offset_4(Series): signal J(n-4) series.
        **cal_args(**dict): factor calculating arguments, including: symbols, target_date, data.

    Returns:
        Series: signal ZQ(n) series.
    """
    origin_offset = cal_args.get('offset', 0)
    if j_series is None:
        j_series = calculate_signal_j(**cal_args)
    if j_series_offset_1 is None:
        cal_args['offset'] = origin_offset - 1
        j_series_offset_1 = calculate_signal_j(**cal_args)
    if j_series_offset_2 is None:
        cal_args['offset'] = origin_offset - 2
        j_series_offset_2 = calculate_signal_j(**cal_args)
    if j_series_offset_3 is None:
        cal_args['offset'] = origin_offset - 3
        j_series_offset_3 = calculate_signal_j(**cal_args)
    if j_series_offset_4 is None:
        cal_args['offset'] = origin_offset - 4
        j_series_offset_4 = calculate_signal_j(**cal_args)
    return j_series + j_series_offset_1 + j_series_offset_2 + j_series_offset_3 + j_series_offset_4


__all__ = [
    'calculate_signal_m',
    'calculate_signal_w',
    'calculate_signal_d',
    'calculate_signal_m1',
    'calculate_signal_m2',
    'calculate_signal_m3',
    'calculate_signal_m4',
    'calculate_signal_w1',
    'calculate_signal_w2',
    'calculate_signal_w3',
    'calculate_signal_w4',
    'calculate_signal_d1',
    'calculate_signal_d2',
    'calculate_signal_d3',
    'calculate_signal_d4',
    'calculate_signal_j',
    'calculate_signal_m2l',
    'calculate_signal_w2l',
    'calculate_signal_d2l',
    'calculate_signal_m4l',
    'calculate_signal_w4l',
    'calculate_signal_d4l',
    'calculate_signal_m2b',
    'calculate_signal_w2b',
    'calculate_signal_d2b',
    'calculate_signal_m4b',
    'calculate_signal_w4b',
    'calculate_signal_d4b',
    'calculate_signal_z',
    'calculate_signal_wz',
    'calculate_signal_t',
    'calculate_signal_zq'
]
