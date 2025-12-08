import pycbc
import numpy
from pycbc import waveform
from scipy.interpolate import CubicSpline


def amplitude_phase_modification_fd(**kwds):
    """
    This function applies the Amplitude-Phase modification, described in
    Kumar, Melching, Ohme (2025), to the base waveform approximant in 
    frequency domain.

    Input in kwds:
     error_in_phase: 'relative' or 'absolute'
                    This argument specify the type of errors to be
                    applied.
     baseline_approximant: FD approximant of the reference waveform model to 
                    modified.
     modification_type: 'cubic_spline', 'cubic_spline_nodes', or 'constant_shift'
                    'cubic_spline': If this option is passed, the dictionary should 
                        includes array of delta_amplitude, delta_phase, and nodal_points
                    'cubic_spline_nodes': When we specify this modification_type, the lower
                        and upper limits of the frequency should be given along with number
                        of nodal points to use.
                    'constant_shift': This option is for the simplest case where there is no
                        frequency dependence of the parameters delta_amplitue and delta_phase.
                        We apply same delta_amplitude and delta_phase for all the frequencies.

    Output:
     h_plus, h_cross
    """
    if kwds['error_in_phase'] not in ['relative', 'absolute']:
        raise ValueError(
            'Only two types of errors are supported, `\'relative\' and `\'absolute\'`.'
        )

    # Baseline WF parameters
    baseline_wf_params = kwds.copy()
    baseline_wf_params['approximant'] = kwds['baseline_approximant']
    hp, hc = waveform.get_fd_waveform(baseline_wf_params)
    dict_waveform_modification = kwds

    if dict_waveform_modification['modification_type'] == 'cubic_spline':
        wf_nodal_points = dict_waveform_modification['nodal_points']
        delta_amplitude_arr = dict_waveform_modification['delta_amplitude']
        delta_phase_arr = dict_waveform_modification['delta_phase']
        delta_amplitude_interp = CubicSpline(wf_nodal_points, delta_amplitude_arr)
        delta_phase_interp = CubicSpline(wf_nodal_points, delta_phase_arr)

        # Calculating amplitude and phase in base WF model and modifying
        # Plus and Cross Polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp) * (
            1 + delta_amplitude_interp(hp.sample_frequencies)
        )
        Am_cross = waveform.amplitude_from_frequencyseries(hc) * (
            1 + delta_amplitude_interp(hc.sample_frequencies)
        )

        if dict_waveform_modification['error_in_phase'] == 'relative':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) * (1 + delta_phase_interp(hp.sample_frequencies))
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) * (1 + delta_phase_interp(hc.sample_frequencies))
        elif dict_waveform_modification['error_in_phase'] == 'absolute':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) + delta_phase_interp(hp.sample_frequencies)
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) + delta_phase_interp(hc.sample_frequencies)

    elif dict_waveform_modification['modification_type'] == 'constant_shift':
        delta_amplitude = dict_waveform_modification['delta_amplitude']
        delta_phase = dict_waveform_modification['delta_phase']

        # Calculating amplitude and phase in base WF model and modifying
        # Plus and Cross Polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp) * (1 + delta_amplitude)
        Am_cross = waveform.amplitude_from_frequencyseries(hc) * (1 + delta_amplitude)

        if dict_waveform_modification['error_in_phase'] == 'relative':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) * (1 + delta_phase)
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) * (1 + delta_phase)
        elif dict_waveform_modification['error_in_phase'] == 'absolute':
            Ph_plus = (
                waveform.phase_from_frequencyseries(hp, remove_start_phase=False)
                + delta_phase
            )
            Ph_cross = (
                waveform.phase_from_frequencyseries(hc, remove_start_phase=False)
                + delta_phase
            )
    elif dict_waveform_modification['modification_type'] == 'cubic_spline_nodes':
        f_lower = (dict_waveform_modification.get('f_lower_wferror',
            default=dict_waveform_modification['f_lower']
            )
        f_high_wferror = dict_waveform_modification['f_high_wferror']
        n_nodes_wferror = int(dict_waveform_modification['n_nodes_wferror'])
        wf_nodal_points = numpy.logspace(
            numpy.log10(f_lower), numpy.log10(f_high_wferror), n_nodes_wferror
        )
        delta_amplitude_arr = numpy.hstack(
            [
                dict_waveform_modification['wferror_amplitude_{}'.format(i)]
                for i in range(len(wf_nodal_points))
            ]
        )
        delta_phase_arr = numpy.hstack(
            [
                dict_waveform_modification['wferror_phase_{}'.format(i)]
                for i in range(len(wf_nodal_points))
            ]
        )

        delta_amplitude_interp = CubicSpline(wf_nodal_points, delta_amplitude_arr)
        delta_phase_interp = CubicSpline(wf_nodal_points, delta_phase_arr)

        # Calculating amplitude and phase in base WF model and modifying
        # Plus and Cross Polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp) * (
            1 + delta_amplitude_interp(hp.sample_frequencies)
        )
        Am_cross = waveform.amplitude_from_frequencyseries(hc) * (
            1 + delta_amplitude_interp(hc.sample_frequencies)
        )

        if dict_waveform_modification['error_in_phase'] == 'relative':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) * (1 + delta_phase_interp(hp.sample_frequencies))
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) * (1 + delta_phase_interp(hc.sample_frequencies))
        elif dict_waveform_modification['error_in_phase'] == 'absolute':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) + delta_phase_interp(hp.sample_frequencies)
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) + delta_phase_interp(hc.sample_frequencies)

    else:
        raise TypeError("Currently, No other modification are supported")

    # Applying the correction in base model.
    hp.data = numpy.vectorize(complex)(
        Am_plus * numpy.cos(Ph_plus), Am_plus * numpy.sin(Ph_plus)
    )
    hc.data = numpy.vectorize(complex)(
        Am_cross * numpy.cos(Ph_cross), Am_cross * numpy.sin(Ph_cross)
    )

    return hp, hc

def amplitude_phase_modification_both_polarization_fd(**kwds):
    """Modify amplitude and phase of waveform polarizations in frequency domain."""

    # Baseline waveform parameters
    baseline_wf_params = kwds.copy()
    baseline_wf_params['approximant'] = kwds['baseline_approximant']

    hp, hc = waveform.get_fd_waveform(baseline_wf_params)

    dict_waveform_modification = kwds.copy()
    modification_type = dict_waveform_modification['modification_type']

    if modification_type == 'cubic_spline':
        wf_nodal_points = dict_waveform_modification['nodal_points']

        delta_amplitude_plus_arr = dict_waveform_modification['delta_amplitude_plus']
        delta_phase_plus_arr = dict_waveform_modification['delta_phase_plus']
        delta_amplitude_plus_interp = CubicSpline(
            wf_nodal_points, delta_amplitude_plus_arr
        )
        delta_phase_plus_interp = CubicSpline(
            wf_nodal_points, delta_phase_plus_arr
        )

        delta_amplitude_cross_arr = dict_waveform_modification['delta_amplitude_cross']
        delta_phase_cross_arr = dict_waveform_modification['delta_phase_cross']
        delta_amplitude_cross_interp = CubicSpline(
            wf_nodal_points, delta_amplitude_cross_arr
        )
        delta_phase_cross_interp = CubicSpline(
            wf_nodal_points, delta_phase_cross_arr
        )

        # Modify amplitude and phase for Plus and Cross polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp) * (
            1 + delta_amplitude_plus_interp(hp.sample_frequencies)
        )
        Am_cross = waveform.amplitude_from_frequencyseries(hc) * (
            1 + delta_amplitude_cross_interp(hc.sample_frequencies)
        )

        if dict_waveform_modification['error_in_phase'] == 'relative':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) * (1 + delta_phase_plus_interp(hp.sample_frequencies))
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) * (1 + delta_phase_cross_interp(hc.sample_frequencies))
        elif dict_waveform_modification['error_in_phase'] == 'absolute':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) + delta_phase_plus_interp(hp.sample_frequencies)
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) + delta_phase_cross_interp(hc.sample_frequencies)

    elif modification_type == 'constant_shift':
        delta_amplitude_plus = dict_waveform_modification['delta_amplitude_plus']
        delta_phase_plus = dict_waveform_modification['delta_phase_plus']

        delta_amplitude_cross = dict_waveform_modification['delta_amplitude_cross']
        delta_phase_cross = dict_waveform_modification['delta_phase_cross']

        # Modify amplitude and phase for Plus and Cross polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp) * (1 + delta_amplitude_plus)
        Am_cross = waveform.amplitude_from_frequencyseries(hc) * (1 + delta_amplitude_cross)

        if dict_waveform_modification['error_in_phase'] == 'relative':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) * (1 + delta_phase_plus)
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) * (1 + delta_phase_cross)
        elif dict_waveform_modification['error_in_phase'] == 'absolute':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) + delta_phase_plus
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) + delta_phase_cross

    elif modification_type == 'cubic_spline_nodes':
        f_lower = (dict_waveform_modification.get('f_lower_wferror', 
            default=dict_waveform_modification['f_lower']
            )
        f_high_wferror = dict_waveform_modification['f_high_wferror']
        n_nodes_wferror = int(dict_waveform_modification['n_nodes_wferror'])

        wf_nodal_points = numpy.logspace(
            numpy.log10(f_lower), numpy.log10(f_high_wferror), n_nodes_wferror
        )

        delta_amplitude_plus_arr = numpy.hstack([
            dict_waveform_modification[f'wferror_amplitude_plus_{i}']
            for i in range(len(wf_nodal_points))
        ])
        delta_phase_plus_arr = numpy.hstack([
            dict_waveform_modification[f'wferror_phase_plus_{i}']
            for i in range(len(wf_nodal_points))
        ])
        delta_amplitude_cross_arr = numpy.hstack([
            dict_waveform_modification[f'wferror_amplitude_cross_{i}']
            for i in range(len(wf_nodal_points))
        ])
        delta_phase_cross_arr = numpy.hstack([
            dict_waveform_modification[f'wferror_phase_cross_{i}']
            for i in range(len(wf_nodal_points))
        ])

        delta_amplitude_plus_interp = CubicSpline(
            wf_nodal_points, delta_amplitude_plus_arr
        )
        delta_phase_plus_interp = CubicSpline(wf_nodal_points, delta_phase_plus_arr)
        delta_amplitude_cross_interp = CubicSpline(
            wf_nodal_points, delta_amplitude_cross_arr
        )
        delta_phase_cross_interp = CubicSpline(
            wf_nodal_points, delta_phase_cross_arr
        )

        # Modify amplitude and phase for Plus and Cross polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp) * (
            1 + delta_amplitude_plus_interp(hp.sample_frequencies)
        )
        Am_cross = waveform.amplitude_from_frequencyseries(hc) * (
            1 + delta_amplitude_cross_interp(hc.sample_frequencies)
        )

        if dict_waveform_modification['error_in_phase'] == 'relative':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) * (1 + delta_phase_plus_interp(hp.sample_frequencies))
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) * (1 + delta_phase_cross_interp(hc.sample_frequencies))
        elif dict_waveform_modification['error_in_phase'] == 'absolute':
            Ph_plus = waveform.phase_from_frequencyseries(
                hp, remove_start_phase=False
            ) + delta_phase_plus_interp(hp.sample_frequencies)
            Ph_cross = waveform.phase_from_frequencyseries(
                hc, remove_start_phase=False
            ) + delta_phase_cross_interp(hc.sample_frequencies)

    else:
        raise TypeError("Currently, no other modification are supported")

    # Apply the correction to the base model
    hp.data = numpy.vectorize(complex)(Am_plus * numpy.cos(Ph_plus),
                                       Am_plus * numpy.sin(Ph_plus))
    hc.data = numpy.vectorize(complex)(Am_cross * numpy.cos(Ph_cross),
                                       Am_cross * numpy.sin(Ph_cross))

    return hp, hc

