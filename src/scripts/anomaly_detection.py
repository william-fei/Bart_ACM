import numpy as np
import pandas as pd
import datetime

import torch
from torch import nn, optim
import torch.nn.functional as F

from splunk_search import search_autoencoder_input
from autoencoder import RecurrentAutoencoder, create_dataset, predict
from gmail_alerts import gmail_send_message

def main():
    # Login to Splunk server and get dataset
    HOST = "localhost"
    PORT = 8080
    USERNAME = "admin"
    PASSWORD = "changed!"
    df = search_autoencoder_input(HOST, PORT, USERNAME, PASSWORD)
    
    # drop non-numerical columns
    temp_df = df.drop(columns=['loc', 'start', 'end'])
    
    # create input for autoencoder
    input_df, seq_len, n_features = create_dataset(temp_df)
    
    # use GPU if available
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    
    # load autoencoder model
    MODEL_PATH = '../../model/ac_anomaly_autoencoder_model_state_dict.pth_20230310-040550'
    embedding_num = 64

    model = RecurrentAutoencoder(seq_len, n_features, embedding_num, device)
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()
    model.to(device)
    
    # classification
    THRESHOLD = 150 # abnormal if loss is less than THRESHOLD
    pred, losses = predict(model, input_df, device)
    is_abnormal = np.array(losses) < THRESHOLD
    results = df[['loc', 'start', 'end']]
    results.insert(loc = 3, column = 'is_abnormal', value = is_abnormal)
    anomalies_df = results[results['is_abnormal']]
    
    # send alerts
    sender = "devtatsuyak@gmail.com"
    receiver = "tatsuya3327@berkeley.edu"
    for _, anomaly_row in anomalies_df.iterrows():
        subject = "[AC ALERT] Anomaly at " + anomaly_row["loc"]
        content = "AC ALERT \n\n"\
        f"An anomaly detected at the following\n"\
        f"Location: {anomaly_row['loc']}\n"\
        f"Time: {anomaly_row['start']} - {anomaly_row['end']}"

        gmail_send_message(sender, receiver, subject, content)

    # save results in csv format
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    RESULT_PATH = '../../data/results/ac_anomaly_autoencoder_results_' + timestamp + '.csv'
    results.to_csv(RESULT_PATH)

    print("Done")
        
if __name__ == "__main__":
    main()
    