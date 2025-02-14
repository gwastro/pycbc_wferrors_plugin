
import pycbc
import numpy
from pycbc import waveform
from scipy.interpolate import CubicSpline

def amplitude_phase_modification_fd(**kwds):
    if kwds['error_in_phase'] not in ['relative', 'absolute']:
        raise ValueError(
            'Only two types of errors are supported, `\'relative\' and `\'absolute\'`.'
        )

    # Baseline WF parameters
    baseline_wf_params = kwds.copy()
    baseline_wf_params['approximant']=kwds['baseline_approximant']
    hp, hc = waveform.get_fd_waveform(baseline_wf_params)
    dict_waveform_modification = kwds#.copy()  # TODO: can't we avoid these operations?
    if dict_waveform_modification['modification_type']=='cubic_spline':
        wf_nodal_points = dict_waveform_modification['nodal_points']
        delta_amplitude_arr = dict_waveform_modification['delta_amplitude']
        delta_phase_arr = dict_waveform_modification['delta_phase']
        delta_amplitude_interp = CubicSpline(wf_nodal_points, delta_amplitude_arr)
        delta_phase_interp = CubicSpline(wf_nodal_points, delta_phase_arr)

        # Calculating amplitude and phase in base WF model and modifying
        # Plus and Cross Polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp)*(1+delta_amplitude_interp(hp.sample_frequencies))
        Am_cross = waveform.amplitude_from_frequencyseries(hc)*(1+delta_amplitude_interp(hc.sample_frequencies))
        if dict_waveform_modification['error_in_phase']=='relative':
            Ph_plus = waveform.phase_from_frequencyseries(hp, remove_start_phase=False)*(1+delta_phase_interp(hp.sample_frequencies))
            Ph_cross = waveform.phase_from_frequencyseries(hc, remove_start_phase=False)*(1+delta_phase_interp(hc.sample_frequencies))
        elif dict_waveform_modification['error_in_phase']=='absolute':
            Ph_plus = waveform.phase_from_frequencyseries(hp, remove_start_phase=False)+delta_phase_interp(hp.sample_frequencies)
            Ph_cross = waveform.phase_from_frequencyseries(hc, remove_start_phase=False)+delta_phase_interp(hc.sample_frequencies)

    elif dict_waveform_modification['modification_type']=='constant_shift':
        delta_amplitude = dict_waveform_modification['delta_amplitude']
        delta_phase = dict_waveform_modification['delta_phase']

        # Calculating amplitude and phase in base WF model and modifying
        # Plus and Cross Polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp)*(1+delta_amplitude)
        Am_cross = waveform.amplitude_from_frequencyseries(hc)*(1+delta_amplitude)
        if dict_waveform_modification['error_in_phase']=='relative':
            Ph_plus = waveform.phase_from_frequencyseries(hp, remove_start_phase=False)*(1+delta_phase)
            Ph_cross = waveform.phase_from_frequencyseries(hc, remove_start_phase=False)*(1+delta_phase)
        elif dict_waveform_modification['error_in_phase']=='absolute':
            Ph_plus = waveform.phase_from_frequencyseries(hp, remove_start_phase=False)+delta_phase
            Ph_cross = waveform.phase_from_frequencyseries(hc, remove_start_phase=False)+delta_phase

        # Applying the correction in base model.
        #hp.data = numpy.vectorize(complex)(Am_plus*numpy.cos(Ph_plus), Am_plus*numpy.sin(Ph_plus))
        #hc.data = numpy.vectorize(complex)(Am_cross*numpy.cos(Ph_cross), Am_cross*numpy.sin(Ph_cross))

    elif dict_waveform_modification['modification_type']=='cubic_spline_nodes':
        f_lower = dict_waveform_modification['f_lower']
        f_high_wferror = dict_waveform_modification['f_high_wferror']
        n_nodes_wferror = int(dict_waveform_modification['n_nodes_wferror'])
        wf_nodal_points = numpy.logspace(numpy.log10(f_lower), numpy.log10(f_high_wferror), n_nodes_wferror)
        delta_amplitude_arr = numpy.hstack([dict_waveform_modification['wferror_amplitude_{}'.format(i)] for i in range(len(wf_nodal_points))])
        delta_phase_arr = numpy.hstack([dict_waveform_modification['wferror_phase_{}'.format(i)] for i in range(len(wf_nodal_points))])
        delta_amplitude_interp = CubicSpline(wf_nodal_points, delta_amplitude_arr)
        delta_phase_interp = CubicSpline(wf_nodal_points, delta_phase_arr)

        # Calculating amplitude and phase in base WF model and modifying
        # Plus and Cross Polarization
        Am_plus = waveform.amplitude_from_frequencyseries(hp)*(1+delta_amplitude_interp(hp.sample_frequencies))
        Am_cross = waveform.amplitude_from_frequencyseries(hc)*(1+delta_amplitude_interp(hc.sample_frequencies))
        if dict_waveform_modification['error_in_phase']=='relative':
            Ph_plus = waveform.phase_from_frequencyseries(hp, remove_start_phase=False)*(1+delta_phase_interp(hp.sample_frequencies))
            Ph_cross = waveform.phase_from_frequencyseries(hc, remove_start_phase=False)*(1+delta_phase_interp(hc.sample_frequencies))
        elif dict_waveform_modification['error_in_phase']=='absolute':
            Ph_plus = waveform.phase_from_frequencyseries(hp, remove_start_phase=False)+delta_phase_interp(hp.sample_frequencies)
            Ph_cross = waveform.phase_from_frequencyseries(hc, remove_start_phase=False)+delta_phase_interp(hc.sample_frequencies)

    else:
        raise TypeError("Currently: only two types of modification are supported")


    # Applying the correction in base model.
    hp.data = numpy.vectorize(complex)(Am_plus*numpy.cos(Ph_plus), Am_plus*numpy.sin(Ph_plus))
    hc.data = numpy.vectorize(complex)(Am_cross*numpy.cos(Ph_cross), Am_cross*numpy.sin(Ph_cross))

    return hp, hc



