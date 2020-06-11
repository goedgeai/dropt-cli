'''
Reference
---
https://github.com/pytorch/examples/tree/master/mnist
'''

from __future__ import print_function
import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from argparse import ArgumentParser
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
from pathlib import Path
from dropt.util.log import UserLogger


# logger
logger_name = Path(__file__).stem
logger = UserLogger(logger_name)
logger.add_console_handler(logging.INFO)
logger.add_file_handler(logging.INFO, filename=f'{logger_name}.log')


class Net(nn.Module):
    '''Define an NN model.'''
    def __init__(self, hidden_size):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(9216, hidden_size)
        self.fc2 = nn.Linear(hidden_size, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output



def train(args, model, device, train_loader, optimizer, epoch):
    '''Model training.'''
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args['log_interval'] == 0:
            print((f'[{batch_idx*len(data):5d}/{len(train_loader.dataset)} '
                   f'({100.*batch_idx/len(train_loader):3.0f}%)]\t'
                   f'Loss: {loss.item():10.6f}'))


def test(args, model, device, test_loader):
    '''Model testing.'''
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print((f'\nTest set: '
           f'Average loss: {test_loss:8.4f}, '
           f'Accuracy: {correct}/{len(test_loader.dataset):.3f} '
           f'({100.*correct/len(test_loader.dataset):2.0f}%)\n'))

    return test_loss


def run(args):
    '''Evaluate performance of the model with the given parameters.'''
    use_cuda = not args['no_cuda'] and torch.cuda.is_available()

    torch.manual_seed(args['seed'])

    device = torch.device("cuda" if use_cuda else "cpu")

    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data',
            train=True,
            download=True,
            transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))])
        ),
        batch_size=args['batch_size'],
        shuffle=True,
        **kwargs)
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data',
            train=False,
            transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))])
        ),
        batch_size=args['test_batch_size'],
        shuffle=True,
        **kwargs)

    model = Net(hidden_size=args['hidden_size']).to(device)
    optimizer = optim.Adadelta(model.parameters(), lr=args['lr'])

    scheduler = StepLR(optimizer, step_size=1, gamma=args['gamma'])
    for epoch in range(1, args['epochs'] + 1):
        logger.info(f'training epoch: {epoch:3d}/{args["epochs"]}')
        train(args, model, device, train_loader, optimizer, epoch)
        loss = test(args, model, device, test_loader)
        scheduler.step()

    if args['save_model']:
        torch.save(model.state_dict(), 'mnist_cnn.pt')

    logger.info(f'loss: (loss:10.6f)')
    return loss


def param_loader():
    '''Get parameters.'''
    parser = ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, metavar='N', default=64,
                        help='input batch size for training (default: 64)')
    parser.add_argument('--hidden-size', type=int, metavar='N', default=128,
                        help='hidden layer size (default: 128)')
    parser.add_argument('--test-batch-size', type=int, metavar='N', default=1000,
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, metavar='N', default=14,
                        help='number of epochs to train (default: 14)')
    parser.add_argument('--lr', type=float, metavar='LR', default=1.0,
                        help='learning rate (default: 1.0)')
    parser.add_argument('--gamma', type=float, metavar='M', default=0.7,
                        help='Learning rate step gamma (default: 0.7)')
    parser.add_argument('--no-cuda', action='store_true',
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, metavar='S', default=1,
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, metavar='N', default=10,
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-model', action='store_true',
                        help='For Saving the current Model')

    args, _ = parser.parse_known_args()
    return vars(args)


if __name__ == '__main__':
    params = param_loader()
    logger.info(f'parameters = {params}')
    print(run(params))
