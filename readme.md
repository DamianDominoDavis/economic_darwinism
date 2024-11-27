# economic_darwinism

A hybrid maching learning approach to the board game Monopoly!

1. Genetic algorithms explore high-level strategies. Likely examples include a preference for orange and railroad properties, or to minimize opponents' earning power.
2. Multi-agent reinforcement learning trains players at tactical decision-making. These include judging a trade, and when to withdraw from auction or decline to start one. Supervised learning will speed initial development.
3. Feed RL-trained strategies back into the GA.

Things we'll need:
* a monopoly sim *(OpenAI Gym?)*
* board & player state logging
* RL libraries *(PyTorch Stable-Baselines3? something in TensorFlow?)*
* SL models
* RL agent structures* GA libraries *(DEAP? PyGAD?)*
* genome definitions
