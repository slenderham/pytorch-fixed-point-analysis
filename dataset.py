"""generating input and target"""

import numpy as np
import torch.utils.data as data


class SineWave(data.Dataset):
    def __init__(self, time_length=200, freq_range=3):
        self.time_length = time_length
        self.freq_range = freq_range

    def __len__(self):
        return 200

    def __getitem__(self, item):
        freq = np.random.randint(1, self.freq_range + 1)
        const_signal = np.repeat(freq / self.freq_range + 0.25, self.time_length)
        const_signal = np.expand_dims(const_signal, axis=1)
        t = np.arange(0, self.time_length*0.025, 0.025)
        target = np.sin(freq * t)
        target = np.expand_dims(target, axis=1)
        return const_signal, target


class Torus(data.Dataset):
    def __init__(self, time_length=50, freq_range=3):
        self.time_length = time_length
        self.freq_range = freq_range

    def __len__(self):
        return 200

    def __getitem__(self, item):
        freq1 = np.random.randint(1, self.freq_range + 1)
        freq2 = 2
        const_signal1 = np.repeat(freq1 / self.freq_range + 0.25, self.time_length)
        const_signal2 = np.repeat(freq2 / self.freq_range + 0.25, self.time_length)
        const_signal1 = np.expand_dims(const_signal1, axis=1)
        const_signal2 = np.expand_dims(const_signal2, axis=1)
        const_signal = np.concatenate((const_signal1, const_signal2), axis=1)
        t = np.arange(0, self.time_length * 0.3, 0.3)
        target = 0.6 * np.sin(2.2 * freq1 * t) + 0.8 * np.sin(0.5 * freq2 * t)
        target = np.expand_dims(target, axis=1)
        return const_signal, target


class TorusPhase(data.Dataset):
    def __init__(self, time_length=50, freq_range=3):
        self.time_length = time_length
        self.freq_range = freq_range

    def __len__(self):
        return 200

    def __getitem__(self, item):
        freq1 = np.random.randint(1, self.freq_range + 1)
        freq2 = 2
        u_3 = np.random.rand()

        const_signal1 = np.repeat(freq1 / self.freq_range + 0.25, self.time_length)
        const_signal2 = np.repeat(freq2 / self.freq_range + 0.25, self.time_length)
        u_3_input = np.repeat(u_3 / 5, 5)
        u_3_rest = np.zeros(self.time_length - 5)
        signal3 = np.concatenate((u_3_input, u_3_rest), axis=0)
        const_signal1 = np.expand_dims(const_signal1, axis=1)
        const_signal2 = np.expand_dims(const_signal2, axis=1)
        signal3 = np.expand_dims(signal3, axis=1)
        const_signal = np.concatenate((const_signal1, const_signal2), axis=1)
        const_signal = np.concatenate((const_signal, signal3), axis=1)

        t = np.arange(0, self.time_length * 0.3, 0.3)
        target = 0.6 * np.sin(2.2 * freq1 * t - (u_3 * np.pi)) + 0.8 * np.sin(0.5 * freq2 * t)
        target = np.expand_dims(target, axis=1)
        return const_signal, target


class TorusAmp(data.Dataset):
    def __init__(self, time_length=50, freq_range=3):
        self.time_length = time_length
        self.freq_range = freq_range

    def __len__(self):
        return 200

    def __getitem__(self, item):
        freq1 = np.random.randint(1, self.freq_range + 1)
        freq2 = 2
        u_3 = np.random.rand()

        const_signal1 = np.repeat(freq1 / self.freq_range + 0.25, self.time_length)
        const_signal2 = np.repeat(freq2 / self.freq_range + 0.25, self.time_length)
        u_3_input = np.repeat(u_3 / 5, 5)
        u_3_rest = np.zeros(self.time_length - 5)
        signal3 = np.concatenate((u_3_input, u_3_rest), axis=0)
        const_signal1 = np.expand_dims(const_signal1, axis=1)
        const_signal2 = np.expand_dims(const_signal2, axis=1)
        signal3 = np.expand_dims(signal3, axis=1)
        const_signal = np.concatenate((const_signal1, const_signal2), axis=1)
        const_signal = np.concatenate((const_signal, signal3), axis=1)

        t = np.arange(0, self.time_length * 0.3, 0.3)
        target = (0.6 + u_3) * np.sin(2.2 * freq1 * t) + 0.8 * np.sin(0.5 * freq2 * t)
        target = np.expand_dims(target, axis=1)
        return const_signal, target


class FlipFlop(data.Dataset):
    def __init__(self, time_length, u_fast_mean=4, u_slow_mean=16):
        self.time_length = time_length
        self.u_fast_mean = u_fast_mean
        self.u_slow_mean = u_slow_mean

    def __len__(self):
        return 200

    def __getitem__(self, item):
        # input signal
        u_fast_signal = np.zeros(self.time_length)
        u_slow_signal = np.zeros(self.time_length)
        fast_signal_timing = np.random.poisson(self.u_fast_mean, 100)
        slow_signal_timing = np.random.poisson(self.u_slow_mean, 100)
        slow_signal_timing[0] = 10
        u_fast_signal[0] = np.random.choice([-1, 1])
        u_slow_signal[0] = np.random.choice([-1, 1])
        count = 0
        index = 0
        while index < self.time_length:
            index += max(0, fast_signal_timing[count])
            count += 1
            if index < self.time_length:
                u_fast_signal[index] = np.random.choice([-1, 1])

        count = 0
        index = 0
        while index < self.time_length:
            index += max(0, slow_signal_timing[count])
            count += 1
            if index < self.time_length:
                u_slow_signal[index] = np.random.choice([-1, 1])

        # target
        fast_signal_record = np.zeros(self.time_length)
        slow_signal_record = np.zeros(self.time_length)
        fast_signal_record[0] = u_fast_signal[0]
        temporal_memory = u_slow_signal[0]
        for index in range(1, self.time_length):
            if u_fast_signal[index] == 0:
                fast_signal_record[index] = fast_signal_record[index - 1]
            else:
                fast_signal_record[index] = u_fast_signal[index]

            if u_slow_signal[index] == 0:
                slow_signal_record[index] = slow_signal_record[index - 1]
            else:
                slow_signal_record[index] = temporal_memory
                temporal_memory = u_slow_signal[index]

        target_signal = np.zeros(self.time_length)
        for index in range(self.time_length):
            target_signal[index] = slow_signal_record[index] * fast_signal_record[index]

        fast_signal = np.expand_dims(u_fast_signal, axis=1)
        slow_signal = np.expand_dims(u_slow_signal, axis=1)
        input_signal = np.concatenate((fast_signal, slow_signal), axis=1)
        target_signal = np.expand_dims(target_signal, axis=1)

        return input_signal, target_signal


class ThreeBitFlipFlop(data.Dataset):
    def __init__(self, time_length, u1_mean=10, u2_mean=10, u3_mean=10):
        self.time_length = time_length
        self.u1_mean = u1_mean
        self.u2_mean = u2_mean
        self.u3_mean = u3_mean

    def __len__(self):
        return 200

    def __getitem__(self, item):
        # input signal
        u1_signal = np.zeros(self.time_length)
        u2_signal = np.zeros(self.time_length)
        u3_signal = np.zeros(self.time_length)
        u1_signal_timing = np.random.poisson(self.u1_mean, self.time_length)
        u2_signal_timing = np.random.poisson(self.u2_mean, self.time_length)
        u3_signal_timing = np.random.poisson(self.u3_mean, self.time_length)

        u1_signal[0] = np.random.choice([-1, 1])
        u2_signal[0] = np.random.choice([-1, 1])
        u3_signal[0] = np.random.choice([-1, 1])
        count = 0
        index = 0
        while index < self.time_length:
            index += max(0, u1_signal_timing[count])
            count += 1
            if index < self.time_length:
                u1_signal[index] = np.random.choice([-1, 1])
        count = 0
        index = 0
        while index < self.time_length:
            index += max(0, u2_signal_timing[count])
            count += 1
            if index < self.time_length:
                u2_signal[index] = np.random.choice([-1, 1])
        count = 0
        index = 0
        while index < self.time_length:
            index += max(0, u3_signal_timing[count])
            count += 1
            if index < self.time_length:
                u3_signal[index] = np.random.choice([-1, 1])

        # target
        u1_signal_record = np.zeros(self.time_length)
        u2_signal_record = np.zeros(self.time_length)
        u3_signal_record = np.zeros(self.time_length)
        u1_signal_record[0] = u1_signal[0]
        u2_signal_record[0] = u2_signal[0]
        u3_signal_record[0] = u3_signal[0]
        for index in range(1, self.time_length):
            if u1_signal[index] == 0:
                u1_signal_record[index] = u1_signal_record[index - 1]
            else:
                u1_signal_record[index] = u1_signal[index]
            if u2_signal[index] == 0:
                u2_signal_record[index] = u2_signal_record[index - 1]
            else:
                u2_signal_record[index] = u2_signal[index]
            if u3_signal[index] == 0:
                u3_signal_record[index] = u3_signal_record[index - 1]
            else:
                u3_signal_record[index] = u3_signal[index]

        z1_target = np.zeros(self.time_length)
        z2_target = np.zeros(self.time_length)
        z3_target = np.zeros(self.time_length)
        for index in range(self.time_length):
            z1_target[index] = u1_signal_record[index]
            z2_target[index] = u2_signal_record[index]
            z3_target[index] = u3_signal_record[index]

        u1_signal = np.expand_dims(u1_signal, axis=1)
        u2_signal = np.expand_dims(u2_signal, axis=1)
        u3_signal = np.expand_dims(u3_signal, axis=1)
        input_signal = np.concatenate((u1_signal, u2_signal), axis=1)
        input_signal = np.concatenate((input_signal, u3_signal), axis=1)
        z1_target = np.expand_dims(z1_target, axis=1)
        z2_target = np.expand_dims(z2_target, axis=1)
        z3_target = np.expand_dims(z3_target, axis=1)
        target_signal = np.concatenate((z1_target, z2_target, z3_target), axis=1)

        return input_signal, target_signal


class ThreeBitFlipFlopMixed(data.Dataset):
    def __init__(self, time_length, u1_mean=10, u2_mean=10, u3_mean=10):
        self.time_length = time_length
        self.u1_mean = u1_mean
        self.u2_mean = u2_mean
        self.u3_mean = u3_mean

    def __len__(self):
        return 200

    def __getitem__(self, item):
        # input signal
        u1_signal = np.zeros(self.time_length)
        u2_signal = np.zeros(self.time_length)
        u3_signal = np.zeros(self.time_length)
        u1_signal_timing = np.random.poisson(self.u1_mean, self.time_length)
        u2_signal_timing = np.random.poisson(self.u2_mean, self.time_length)
        u3_signal_timing = np.random.poisson(self.u3_mean, self.time_length)

        u1_signal[0] = np.random.choice([-1, 1])
        u2_signal[0] = np.random.choice([-1, 1])
        u3_signal[0] = np.random.choice([-1, 1])
        count = 0
        index = 0
        while index < self.time_length:
            index += max(0, u1_signal_timing[count])
            count += 1
            if index < self.time_length:
                u1_signal[index] = np.random.choice([-1, 1])
        count = 0
        index = 0
        while index < self.time_length:
            index += max(0, u2_signal_timing[count])
            count += 1
            if index < self.time_length:
                u2_signal[index] = np.random.choice([-1, 1])
        count = 0
        index = 0
        while index < self.time_length:
            index += max(0, u3_signal_timing[count])
            count += 1
            if index < self.time_length:
                u3_signal[index] = np.random.choice([-1, 1])

        # target
        u1_signal_record = np.zeros(self.time_length)
        u2_signal_record = np.zeros(self.time_length)
        u3_signal_record = np.zeros(self.time_length)
        u1_signal_record[0] = u1_signal[0]
        u2_signal_record[0] = u2_signal[0]
        u3_signal_record[0] = u3_signal[0]
        for index in range(1, self.time_length):
            if u1_signal[index] == 0:
                u1_signal_record[index] = u1_signal_record[index - 1]
            else:
                u1_signal_record[index] = u1_signal[index]
            if u2_signal[index] == 0:
                u2_signal_record[index] = u2_signal_record[index - 1]
            else:
                u2_signal_record[index] = u2_signal[index]
            if u3_signal[index] == 0:
                u3_signal_record[index] = u3_signal_record[index - 1]
            else:
                u3_signal_record[index] = u3_signal[index]

        z1_target = np.zeros(self.time_length)
        z2_target = np.zeros(self.time_length)
        z3_target = np.zeros(self.time_length)
        for index in range(self.time_length):
            z1_target[index] = u1_signal_record[index] * u2_signal_record[index]
            z2_target[index] = u2_signal_record[index] * u3_signal_record[index]
            z3_target[index] = u1_signal_record[index] * u2_signal_record[index] * u3_signal_record[index]

        u1_signal = np.expand_dims(u1_signal, axis=1)
        u2_signal = np.expand_dims(u2_signal, axis=1)
        u3_signal = np.expand_dims(u3_signal, axis=1)
        input_signal = np.concatenate((u1_signal, u2_signal), axis=1)
        input_signal = np.concatenate((input_signal, u3_signal), axis=1)
        z1_target = np.expand_dims(z1_target, axis=1)
        z2_target = np.expand_dims(z2_target, axis=1)
        z3_target = np.expand_dims(z3_target, axis=1)
        target_signal = np.concatenate((z1_target, z2_target, z3_target), axis=1)

        return input_signal, target_signal


