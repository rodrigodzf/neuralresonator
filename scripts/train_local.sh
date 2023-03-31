#!/bin/bash

train \
++datamodule.sample_rate=32000 \
++datamodule.batch_size=32 \
++datamodule.num_workers=4 \
++datamodule.train_index_map_path=/media/fast/data/datasets/100_10_1_n_refinements_4/materials_shapes_train/index_map.csv \
++datamodule.val_index_map_path=/media/fast/data/datasets/100_10_1_n_refinements_4/materials_shapes_val/index_map.csv \
++datamodule.test_index_map_path=/media/fast/data/datasets/100_10_1_n_refinements_4/materials_shapes_val/index_map.csv \
++logger.group=multishape-multimaterial \
++trainer.limit_train_batches=2000 \
++trainer.limit_val_batches=0.1 \
++trainer.limit_test_batches=2 \
++trainer.val_check_interval=500 \
seed=3407