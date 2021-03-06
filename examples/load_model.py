import timm

from argus import Model, load_model


class TimmModel(Model):
    nn_module = timm.create_model


class AnotherTimmModel(Model):
    nn_module = timm.create_model


if __name__ == "__main__":
    params = {
        'nn_module': {
            'model_name': 'tf_efficientnet_b0_ns',
            'pretrained': True,
            'num_classes': 10,
            'in_chans': 1,
            'drop_rate': 0.2,
            'drop_path_rate': 0.2
        },
        'optimizer': ('Adam', {'lr': 0.01}),
        'loss': 'CrossEntropyLoss',
        'device': 'cuda'
    }

    model = TimmModel(params)
    model_path = 'model_load.pth'
    model.save(model_path)
    del model

    loaded_model = load_model(model_path)
    print("Load model:", loaded_model.params)

    loaded_model = load_model(
        file_path=model_path,
        nn_module={
            'model_name': 'tf_efficientnet_b0_ns',
            'pretrained': False,
            'num_classes': 10,
            'in_chans': 1,
            'drop_rate': 0.6,
            'drop_path_rate': 0.4
        }
    )
    print("Change nn_module params:", loaded_model.params)

    def pretrain_to_false(params):
        params['nn_module']['pretrained'] = True
        return params

    loaded_model = load_model(model_path, optimizer=None, loss=None,
                              change_params_func=pretrain_to_false)

    print(f"Load model without optimizer '{loaded_model.optimizer}' "
          f"and loss '{loaded_model.loss}'")
    print("Set pretrain to False with 'change_params_func'", loaded_model.params)
    assert loaded_model.predict_ready()
    assert not loaded_model.train_ready()

    loaded_model = load_model(model_path, model_name='AnotherTimmModel')
    assert isinstance(loaded_model, AnotherTimmModel)
    print("Change argus module class:", loaded_model.__class__)
