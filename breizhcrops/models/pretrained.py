INCEPTIONTIME_URL = "https://syncandshare.lrz.de/dl/fi3jqF5niKQJTufETbbBPp8N/InceptionTime_input-dim%3D13_num-classes%3D9_hidden-dims%3D64_num-layers%3D4_learning-rate%3D0.0005930998594456241_weight-decay%3D1.8660112778851542e-05.pth"
LSTM_URL = "https://syncandshare.lrz.de/dl/fiGjW6JtFuiUs6kcRHaYbNUr/LSTM_input-dim%3D13_num-classes%3D9_hidden-dims%3D128_num-layers%3D4_bidirectional%3DTrue_use-layernorm%3DTrue_dropout%3D0.5713020228087161_learning-rate%3D0.009880117756170353_weight-decay%3D5.256755602421856e-07.pth"
MSRESNET_URL = "https://syncandshare.lrz.de/dl/fi6FKvymvpyHZ4JVtyWo64wh/MSResNet_input-dim%3D13_num-classes%3D9_hidden-dims%3D32_learning-rate%3D0.0006271686393146093_weight-decay%3D4.750234747127917e-06.pth"
OMNISCALECNN_URL = "https://syncandshare.lrz.de/dl/fi8BZ53crPbExH79xMpNXop3/OmniScaleCNN_learning-rate%3D0.001057192239267413_weight-decay%3D2.2522895556530792e-07.pth"
STARRNN_URL = "https://syncandshare.lrz.de/dl/fiDxFhPxyFxAUVTJKCbncnnS/StarRNN_input-dim%3D13_num-classes%3D9_hidden-dims%3D128_num-layers%3D3_dropout%3D0.5_learning-rate%3D0.008960989762612663_weight-decay%3D2.2171861339535254e-06.pth"
TEMPCNN_URL = "https://syncandshare.lrz.de/dl/fiVpXRMKiEQKfLFnRrKGFhwV/TempCNN_input-dim%3D13_num-classes%3D9_sequencelenght%3D45_kernelsize%3D7_hidden-dims%3D128_dropout%3D0.18203942949809093_learning-rate%3D0.00023892874563871753_weight-decay%3D5.181869707846283e-05.pth"
TRANSFORMER_URL = "https://syncandshare.lrz.de/dl/fiAuAsPwxZPpyDZZ5fyFrCh8/TransformerEncoder_input-dim%3D13_num-classes%3D9_d-model%3D64_d-inner%3D256_n-layers%3D3_n-head%3D1_dropout%3D0.39907201621346594_learning-rate%3D0.0013144015360979785_weight-decay%3D5.523908582054716e-08.pth"

from .OmniScaleCNN import OmniScaleCNN
from .LongShortTermMemory import LSTM
from .StarRNN import StarRNN
from .InceptionTime import InceptionTime
from .MSResNet import MSResNet
from .TempCNN import TempCNN
from .TransformerModel import TransformerModel
import torch
from ..utils import download_file
import tempfile
import os

def _download_and_load_weights(url, model):
    fd, path = tempfile.mkstemp()
    try:
        download_file(url, output_path=path, overwrite=True)
        model.load_state_dict(torch.load(path, map_location=torch.device('cpu'))["model_state"])
        model.eval()
    finally:
        os.remove(path)

def pretrained(model, device=torch.device("cpu")):
    # make case insensitive
    model = model.lower()

    # fixed parameters of pretrained models
    ndims = 13
    num_classes = 9
    sequencelength = 45
    
    if model == "omniscalecnn":
        model = OmniScaleCNN(input_dim=ndims, num_classes=num_classes, sequencelength=sequencelength).to(device)
        _download_and_load_weights(OMNISCALECNN_URL, model)
        return model
    elif model == "lstm":
        model = LSTM(input_dim=ndims, num_classes=num_classes).to(device)
        _download_and_load_weights(LSTM_URL, model)
        return model
    elif model == "starrnn":
        model = StarRNN(input_dim=ndims,num_classes=num_classes,bidirectional=False,use_batchnorm=False,
                        use_layernorm=True,device=device).to(device)
        _download_and_load_weights(STARRNN_URL, model)
        return model
    elif model == "inceptiontime":
        model = InceptionTime(input_dim=ndims, num_classes=num_classes, device=device).to(device)
        _download_and_load_weights(INCEPTIONTIME_URL, model)
        return model
    elif model == "msresnet":
        model = MSResNet(input_dim=ndims, num_classes=num_classes).to(device)
        _download_and_load_weights(MSRESNET_URL, model)
        return model
    elif model == "transformerencoder" or model == "transformer":
        model = TransformerModel(input_dim=ndims, num_classes=num_classes,
                                 sequencelength=sequencelength,activation="relu").to(device)
        _download_and_load_weights(TRANSFORMER_URL, model)
        return model
    elif model == "tempcnn":
        model = TempCNN(input_dim=ndims, num_classes=num_classes, sequencelength=sequencelength).to(device)
        _download_and_load_weights(TEMPCNN_URL, model)
        return model
    else:
        raise ValueError("invalid model argument")

if __name__ == '__main__':
    pass
