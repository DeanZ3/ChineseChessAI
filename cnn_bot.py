import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import random
import numpy as np
from pieces import avail_move


class CNNBot:
    def __init__(self, color, model, model_path="cnn_model.pth"):
        self.color = color
        self.model = model if model is not None else load_model(model_path)

    def update_board(self, game):
        self.board = game.board
        self.pieces = [p for p in game.pieces if p.color == self.color]

    def encode_board(self):
        board_tensor = torch.zeros((1, BOARD_CHANNELS, BOARD_HEIGHT, BOARD_WIDTH))
        for piece in self.pieces + [
            p for row in self.board for p in row if p and p.color != self.color
        ]:
            idx = self.piece_to_channel(piece)
            x, y = piece.position[0] - 1, piece.position[1] - 1
            board_tensor[0, idx, x, y] = 1
        return board_tensor

    def piece_to_channel(self, piece):
        mapping = {"R": 0, "H": 1, "E": 2, "A": 3, "G": 4, "C": 5, "S": 6}
        offset = 0 if piece.color == "red" else 7
        return mapping[piece.name] + offset

    def move(self):
        legal_moves = []
        piece_map = {}
        for piece in self.pieces:
            moves = avail_move(piece, self.board)
            for move in moves:
                from_idx = (piece.position[0] - 1) * 9 + (piece.position[1] - 1)
                to_idx = (move[0][0] - 1) * 9 + (move[0][1] - 1)
                legal_moves.append((from_idx, to_idx))
                piece_map[(from_idx, to_idx)] = (piece, move)

        if not legal_moves:
            return None, None

        board_tensor = self.encode_board()
        move_idx, _ = select_action(self.model, board_tensor, legal_moves)
        return piece_map[move_idx]


# Constants
BOARD_CHANNELS = 14  # assuming 7 types of pieces * 2 colors
BOARD_HEIGHT = 10
BOARD_WIDTH = 9
MOVE_SPACE = (
    BOARD_HEIGHT * BOARD_WIDTH * BOARD_HEIGHT * BOARD_WIDTH
)  # 8100 possible (from, to) moves


# CNN model
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(BOARD_CHANNELS, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * BOARD_HEIGHT * BOARD_WIDTH, 512)
        self.fc2 = nn.Linear(512, MOVE_SPACE)

    def forward(self, x):
        x = F.relu(self.conv1(x))  # (batch, 32, 10, 9)
        x = F.relu(self.conv2(x))  # (batch, 64, 10, 9)
        x = x.view(x.size(0), -1)  # flatten to (batch, 64*10*9)
        x = F.relu(self.fc1(x))
        return self.fc2(x)  # logits for all possible moves


# Utility functions
def save_model(model, path="cnn_model.pth"):
    torch.save(model.state_dict(), path)


def load_model(path="cnn_model.pth"):
    model = CNN()
    model.load_state_dict(torch.load(path, map_location=torch.device("cpu")))
    model.eval()
    return model


def select_action(model, board_tensor, legal_moves):
    output = model(board_tensor).squeeze()  # (8100,)
    probs = F.softmax(output, dim=0)

    move_indices = [from_ * 90 + to for (from_, to) in legal_moves]
    legal_probs = probs[move_indices]
    legal_probs /= legal_probs.sum()  # renormalize

    dist = torch.distributions.Categorical(legal_probs)
    selected_idx = dist.sample()
    selected_move = legal_moves[selected_idx.item()]
    log_prob = dist.log_prob(selected_idx)
    return selected_move, log_prob


def play_self_game(model):
    # Setup a fake board with randomly placed pieces
    from board import AIAIBoard  # assuming this imports your board class

    game = AIAIBoard()
    bot_r = CNNBot("red", model=model)
    bot_b = CNNBot("black", model=model)

    game.bot_r = bot_r
    game.bot_b = bot_b

    log_probs = []
    rewards = []

    while game.winning is None:
        bot = game.bot_r if game.turn == "red" else game.bot_b
        bot.update_board(game)

        # Gather legal moves
        legal_moves = []
        piece_map = {}
        for piece in bot.pieces:
            moves = avail_move(piece, game.board)
            for move in moves:
                from_idx = (piece.position[0] - 1) * 9 + (piece.position[1] - 1)
                to_idx = (move[0][0] - 1) * 9 + (move[0][1] - 1)
                legal_moves.append((from_idx, to_idx))
                piece_map[(from_idx, to_idx)] = (piece, move)

        if not legal_moves:
            game.winning = "black" if game.turn == "red" else "red"
            break

        # Encode board and select action
        board_tensor = bot.encode_board()
        move_idx, log_prob = select_action(bot.model, board_tensor, legal_moves)
        piece, move = piece_map[move_idx]

        # Apply the move
        game.board[piece.position[0]][piece.position[1]] = None
        piece.position = move[0]
        game.board[move[0][0]][move[0][1]] = piece

        if move[1] is not None:
            captured = move[1]
            game.pieces.remove(captured)
            if captured.name == "G":
                game.winning = bot.color
                break

        game._switch_turn()
        log_probs.append(log_prob)
        rewards.append(0)  # intermediate steps: zero reward

    # Assign final reward to all moves of the winning/losing side
    final_reward = +1 if game.winning == "red" else -1
    rewards = [
        final_reward if i % 2 == 0 else -final_reward for i in range(len(log_probs))
    ]
    print(f"[RESULT] {game.winning.upper()} wins the game.")
    return log_probs, rewards


def train_on_game(model, optimizer, log_probs, rewards, gamma=0.99):
    discounted_rewards = []
    R = 0
    for r in reversed(rewards):
        R = r + gamma * R
        discounted_rewards.insert(0, R)
    discounted_rewards = torch.tensor(discounted_rewards)
    discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (
        discounted_rewards.std() + 1e-5
    )

    loss = 0
    for log_prob, R in zip(log_probs, discounted_rewards):
        loss -= log_prob * R
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


# Main training loop
if __name__ == "__main__":
    model = CNN()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for episode in range(50):
        log_probs, rewards = play_self_game(model)
        train_on_game(model, optimizer, log_probs, rewards)
        print(f"Episode {episode + 1} complete")

    save_model(model)
