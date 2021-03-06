import os
import cPickle
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time
class TestSpeaker:
    #path to training data
    source   = "development_set\\"
    modelpath = "speaker_models\\"
    test_file = "development_set_test.txt"
    def predictSpeaker(self):
        file_paths = open(test_file,'r')

        gmm_files = [os.path.join(modelpath,fname) for fname in
                      os.listdir(modelpath) if fname.endswith('.gmm')]
        fname = os.path.join(modelpath,fname)
        #Load the Gaussian gender Models
        for fname in gmm_files:
            models =  [cPickle.load(open(fname)) for fname in gmm_files]
        speakers   = [fname.split("\\")[-1].split(".gmm")[0] for fname
                      in gmm_files]
        # Read the test directory and get the list of test audio files
        for path in file_paths:

            path = path.strip()
            print path
            sr,audio = read(source + path)
            vector   = extract_features(audio,sr)
            log_likelihood = np.zeros(len(models))

            for i in range(len(models)):
                gmm    = models[i]  #checking with each model one by one
                scores = np.array(gmm.score(vector))
                log_likelihood[i] = scores.sum()
                print log_likelihood[i]

            winner = np.argmax(log_likelihood)
            print "\tdetected as - ", speakers[winner]