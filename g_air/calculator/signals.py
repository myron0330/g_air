"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: signals calculating file.
#   Author: Myron
# **********************************************************************************#
"""
import numpy as np
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

    3.2)        Ws(n) > Ws(n-5) --> 1;       Ws(n) < Ws(n-20) --> -1;      Ws(n) == Ws(n-20) --> 0

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
        w_series(Series): signal W(n) series.
        w_series_offset_5(Series): signal W(n-5) series.
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
    'calculate_signal_w4'
]
