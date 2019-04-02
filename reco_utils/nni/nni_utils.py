import numpy as np
import requests
import time

NNI_REST_ENDPOINT = 'http://localhost:8080/api/v1/nni'
NNI_STATUS_URL = NNI_REST_ENDPOINT + '/check-status'
NNI_TRIAL_JOBS_URL = NNI_REST_ENDPOINT + '/trial-jobs'


def get_experiment_status(status_url):
    nni_status = requests.get(status_url).json()
    return nni_status['status']


def check_experiment_status():
    while True:
        time.sleep(20)
        status = get_experiment_status(NNI_STATUS_URL)
        if status == 'DONE':
            break
        elif status != 'RUNNING':
            raise RuntimeError("NNI experiment failed to complete with status {}".format(status))


def get_trials(optimize_mode):
    if optimize_mode not in ['minimize', 'maximize']:
        raise ValueError("optimize_mode should equal either 'minimize' or 'maximize'")
    all_trials = requests.get(NNI_TRIAL_JOBS_URL).json()
    trials = [(eval(trial['finalMetricData'][0]['data']), trial['logPath']) for trial in all_trials]
    optimize_fn = np.argmax if optimize_mode == 'maximize' else np.argmin
    ind_best = optimize_fn([trial[0]['default'] for trial in trials])
    best_trial = trials[ind_best]
    trial_log_path = trials[-1][1].split(':')[-1]
    return trials, best_trial, trial_log_path
