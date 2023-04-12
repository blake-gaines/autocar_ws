import math
import numpy as np
import os
import torch
import torch.nn as nn
import torch.optim as optim

class cnn1D_plus_velocity(nn.Module):
    def __init__(self, state_size, history_length, num_actions):
        super(cnn1D_plus_velocity, self).__init__()
        self.state_size = state_size
        self.history_length = history_length
        self.num_actions = num_actions
        
        self.conv_layers = nn.Sequential(
            nn.Conv1d(self.history_length, 16, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv1d(16, 32, kernel_size=2, stride=1),
            nn.ReLU(),
            nn.Flatten(),
        )
        
        self.fc_layers = nn.Sequential(
            # nn.Linear(32 * ((self.state_size - 3) // 2 + 1) + self.history_length, 64),
            nn.Linear(258, 64),
            nn.ReLU(),
            nn.Linear(64, self.num_actions)
        )

        self.loss_fn = nn.SmoothL1Loss()
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)
        
    def forward(self, inputs):
        lidar, acc = inputs["lidar"], inputs["acc"]
        # lidar = torch.unsqueeze(lidar, dim=1)
        lidar = lidar.reshape((-1, self.history_length, self.state_size))
        # print("LIDAR SHAPE:", lidar.shape, lidar.dtype)
        # print("ACC SHAPE:", acc.shape, acc.dtype)
        x = self.conv_layers(lidar)
        x = torch.cat([x, acc], dim=1)
        x = self.fc_layers(x)
        return x
        
    # def train_step(self, inputs, input_acceleration, targets):
    #     self.optimizer.zero_grad()
    #     predictions = self(inputs, input_acceleration)
    #     loss = self.loss_fn(predictions, targets)
    #     loss.backward()
    #     self.optimizer.step()
    #     return loss.item()

class cnn2D(nn.Module):
    def __init__(self, image_width, image_height, history_length, num_actions):
        super(cnn2D, self).__init__()
        self.num_actions = num_actions
        self.conv_layers = nn.Sequential(
            nn.Conv2d(history_length, 16, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(16, 8, kernel_size=2, stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.fc_layers = nn.Sequential(
            nn.Linear(8*10*10, 64),
            nn.ReLU(),
            nn.Linear(64, num_actions)
        )

    def forward(self, x):
        x = x.float() / 255
        x = self.conv_layers(x)
        x = x.view(-1, 8*10*10)
        x = self.fc_layers(x)
        return x

class DeepQNetwork:
    def __init__(self, num_actions, state_size, replay_buffer, base_dir, tensorboard_dir, args):
        
        self.num_actions = num_actions
        self.state_size = state_size
        self.replay_buffer = replay_buffer
        self.history_length = args.history_length

        self.learning_rate = args.learning_rate
        self.gamma = args.gamma
        self.target_model_update_freq = args.target_model_update_freq

        self.checkpoint_dir = base_dir + '/models/'

        self.lidar_to_image = args.lidar_to_image
        self.image_width = args.image_width
        self.image_height = args.image_height

        self.add_velocity = args.add_velocity

        if not os.path.isdir(self.checkpoint_dir):
            os.makedirs(self.checkpoint_dir)


        self.behavior_net = self.__build_q_net()
        self.target_net = self.__build_q_net()
        self.behavior_net.double()
        self.target_net.double()

        # model_as_string = []
        # self.target_net.summary(print_fn=lambda x : model_as_string.append(x))
        # "\n".join(model_as_string)

        # summary_writer = tf.summary.create_file_writer(tensorboard_dir)
        # with summary_writer.as_default():
        #     tf.summary.text('model', model_as_string, step=0)

        # if args.model is not None:
        #     self.target_net.load_weights(args.model)
        #     self.behavior_net.set_weights(self.target_net.get_weights())


    def __build_q_net(self):
        if self.lidar_to_image:
            return self.__build_cnn2D()
        else:
            if self.add_velocity:
                return self.__build_cnn1D_plus_velocity()
            else:
                # select from __build_dense or build_cnn1D
                return self.__build_cnn1D()

    def __build_dense(self):
        # inputs = tf.keras.Input(shape=(self.state_size, self.history_length))
        # x = layers.Dense(128, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(inputs)
        # x = layers.Dense(128, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # x = layers.Flatten()(x)
        # predictions = layers.Dense(self.num_actions, activation='linear', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # model = tf.keras.Model(inputs=inputs, outputs=predictions)
        # model.compile(optimizer=optimizers.Adam(self.learning_rate),
        #                     loss=losses.Huber()) #loss to be removed. It is needed in the bugged version installed on Jetson
        # model.summary()
        model = nn.Sequential(
            nn.Linear(self.state_size * self.history_length, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, self.num_actions)
        )
        return model

    def __build_cnn1D(self):
        # inputs = tf.keras.Input(shape=(self.state_size, self.history_length))
        # x = layers.Conv1D(filters=16, kernel_size=4, strides=2, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(inputs)
        # x = layers.Conv1D(filters=32, kernel_size=2, strides=1, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # x = layers.Flatten()(x)
        # x = layers.Dense(64, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # predictions = layers.Dense(self.num_actions, activation='linear', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # model = tf.keras.Model(inputs=inputs, outputs=predictions)
        # model.compile(optimizer=optimizers.Adam(self.learning_rate),
        #                     loss=losses.Huber()) #loss to be removed. It is needed in the bugged version installed on Jetson
        # model.summary()
        
        model = nn.Sequential(
            nn.Conv1d(self.history_length, 16, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv1d(16, 32, kernel_size=2, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32 * ((self.state_size - 3) // 2 + 1), 64),
            nn.ReLU(),
            nn.Linear(64, self.num_actions)
        )

        return model

    def __build_cnn1D_plus_velocity(self):
        # inputs = tf.keras.Input(shape=(self.state_size, self.history_length), name="lidar")
        # input_acceleration = tf.keras.Input(shape=((self.history_length)), name="acc")
        # x = layers.Conv1D(filters=16, kernel_size=4, strides=2, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(inputs)
        # x = layers.Conv1D(filters=32, kernel_size=2, strides=1, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # x = layers.Flatten()(x)
        # x = layers.concatenate([x, input_acceleration])
        # x = layers.Dense(64, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # predictions = layers.Dense(self.num_actions, activation='linear', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # model = tf.keras.Model(inputs=[inputs, input_acceleration], outputs=predictions)
        # model.compile(optimizer=optimizers.Adam(self.learning_rate),
        #                     loss=losses.Huber()) #loss to be removed. It is needed in the bugged version installed on Jetson
        # model.summary()


        return cnn1D_plus_velocity(self.state_size, self.history_length, self.num_actions)

    def __build_cnn2D(self):
        # inputs = tf.keras.Input(shape=(self.image_width, self.image_height, self.history_length))
        # x = layers.Lambda(lambda layer: layer / 255)(inputs)
        # x = layers.Conv2D(filters=16, kernel_size=(4, 4), strides=(2, 2), activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # x = layers.MaxPool2D((2,2))(x)
        # x = layers.Conv2D(filters=8, kernel_size=(2, 2), strides=(1, 1), activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # x = layers.MaxPool2D((2,2))(x)
        # x = layers.Flatten()(x)
        # x = layers.Dense(64, activation='relu', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # predictions = layers.Dense(self.num_actions, activation='linear', kernel_initializer=initializers.VarianceScaling(scale=2.))(x)
        # model = tf.keras.Model(inputs=inputs, outputs=predictions)
        # model.compile(optimizer=optimizers.Adam(self.learning_rate),
        #                     loss=losses.Huber()) #loss to be removed. It is needed in the bugged version installed on Jetson
        # model.summary()
        return cnn2D(self.image_width, self.image_height, self.history_length, self.num_actions)


    def inference(self, state):
        if self.lidar_to_image:
            state = state.reshape((-1, self.image_width, self.image_height, self.history_length))
        elif self.add_velocity:
            old_state, state = state, dict()
            state["lidar"] = torch.from_numpy(old_state[0].reshape((-1, self.state_size, self.history_length)))
            state["acc"] = torch.from_numpy(old_state[1].reshape((-1, self.history_length)))
        else:
            state = state.reshape((-1, self.state_size, self.history_length))

        return self.behavior_predict(state).detach().numpy().argmax(axis=1)

    def train(self, batch, step_number):
        if self.add_velocity:
            old_states_lidar = np.asarray([sample.old_state.get_data()[0] for sample in batch])
            old_states_acc = np.asarray([sample.old_state.get_data()[1] for sample in batch])
            new_states_lidar = np.asarray([sample.new_state.get_data()[0] for sample in batch])
            new_states_acc = np.asarray([sample.new_state.get_data()[1] for sample in batch])
            #actions = np.asarray([sample.action for sample in batch])
            actions = np.asarray([sample.action if isinstance(sample.action, int) else sample.action.item() for sample in batch])
            assert actions.dtype != np.object_, actions
            rewards = np.asarray([sample.reward for sample in batch])
            is_terminal = np.asarray([sample.terminal for sample in batch])

            predicted = self.target_predict({'lidar': torch.from_numpy(np.asarray(new_states_lidar)), 'acc': torch.from_numpy(np.asarray(new_states_acc))})
            q_new_state, _ = torch.max(predicted, axis=1)
            target_q = rewards + (self.gamma*q_new_state.detach().numpy() * (1-is_terminal))
            # one_hot_actions = tf.keras.utils.to_categorical(actions, self.num_actions)# using tf.one_hot causes strange errors
            one_hot_actions = nn.functional.one_hot(torch.from_numpy(actions), int(self.num_actions))

            state = {'lidar': old_states_lidar, 'acc': old_states_acc}
            state = {k: torch.from_numpy(np.asarray(v)) for k,v in state.items()}
            loss = self.gradient_train({'lidar': torch.from_numpy(np.asarray(old_states_lidar)), 'acc': torch.from_numpy(np.asarray(old_states_acc))}, target_q, one_hot_actions)
        else:
            old_states = np.asarray([sample.old_state.get_data() for sample in batch])
            new_states = np.asarray([sample.new_state.get_data() for sample in batch])
            actions = np.asarray([sample.action for sample in batch])
            rewards = np.asarray([sample.reward for sample in batch])
            is_terminal = np.asarray([sample.terminal for sample in batch])

            q_new_state = np.max(self.target_predict(new_states), axis=1)
            target_q = rewards + (self.gamma*q_new_state * (1-is_terminal))
            # one_hot_actions = tf.keras.utils.to_categorical(actions, self.num_actions)# using tf.one_hot causes strange errors
            one_hot_actions = nn.functional.one_hot(actions, self.num_actions)

            loss = self.gradient_train(old_states, target_q, one_hot_actions)

        if step_number % self.target_model_update_freq == 0:
            # self.behavior_net.set_weights(self.target_net.get_weights())
            self.behavior_net.load_state_dict(self.target_net.state_dict())

        return float(loss)

    # @tf.function
    def target_predict(self, state):
        return self.target_net(state)

    # @tf.function
    def behavior_predict(self, state):
        return self.behavior_net(state)

    # @tf.function
    def gradient_train(self, old_states, target_q, one_hot_actions):
        # with tf.GradientTape() as tape:
        #     q_values = self.target_net(old_states)
        #     current_q = tf.reduce_sum(tf.multiply(q_values, one_hot_actions), axis=1)
        #     loss = losses.Huber()(target_q, current_q)

        # variables = self.target_net.trainable_variables
        # gradients = tape.gradient(loss, variables)
        # self.target_net.optimizer.apply_gradients(zip(gradients, variables))
        self.target_net.optimizer.zero_grad()

        q_values = self.target_net(old_states)
        current_q = torch.sum(q_values * one_hot_actions, dim=1)
        loss = nn.functional.smooth_l1_loss(current_q, torch.from_numpy(target_q))

        loss.backward()
        self.target_net.optimizer.step()
        return loss


    def save_network(self):
        # print("saving..")
        # self.target_net.save_weights(self.checkpoint_dir)
        # self.replay_buffer.save()
        # print("saved")
        return
