from gym.envs.registration import register

register(
    id='flipper-v0',
    entry_point='gym_flipper.envs:FlipperEnv',
)
