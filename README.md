
<div align="center">

<h1>
Neural Resonator
</h1>

> Rigid-Body Sound Synthesis with Differentiable Modal Resonators

![GitHub](https://img.shields.io/github/license/rodrigodzf/NeuralResonator.png)
[![arXiv](https://img.shields.io/badge/arXiv-2210.15306-b31b1b.svg)](https://arxiv.org/abs/2210.15306)

</div>

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## About

This is the code for the paper [Rigid-Body Sound Synthesis with
Differentiable Modal Resonators](https://arxiv.org/abs/2210.15306). It
contains the implementation of the differentiable modal resonator
networks, as well as the code to train them and generate the audio
samples used in the paper.

## Install

To install the package, run the following command:

``` sh
pip install -e '.[dev]'
```

## Train

For a quicker preview of the training process, please refer to this
[notebook](../examples/fit_to_arbitrary_shapes.ipynb).

In order to train the network first we need to generate the dataset.
Training the network requires large dataset the generation and the
training might take up to a day to complete. To do so, run the following
command (adjusting the number of shapes and materials to generate):

``` sh
generate_dataset \
n_train_shapes=500 \
n_val_shapes=20 \
n_test_shapes=20 \
n_train_materials=500 \
n_val_materials=20 \
n_test_materials=20 \
++paths.data_dir=./data
```

To train the network, run the following command:

``` sh
train \
++datamodule.sample_rate=32000 \
++datamodule.batch_size=64 \
++datamodule.num_workers=8 \
++datamodule.train_index_map_path=./data/materials_shapes_train/index_map.csv \
++datamodule.val_index_map_path=./data/materials_shapes_val/index_map.csv \
++datamodule.test_index_map_path=./data/materials_shapes_val/index_map.csv \
seed=3407
```