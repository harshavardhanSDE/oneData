# oneData ( Learn Data not the Infra )

A platform automation tool for Data Engineering dev environment. Provision and scale local development clusters using VMs.

CLI for provisioning tools and infrastrucutre for big data application. Only to be used in dev environment, ( Learning purposes ) not for production.

## Usage

### building locally.

using the `build` package to create the `.whl`,

```
python -m build
```

and install locally.

```
pip install dist/provisioner-1.0.0-py3-none-any.whl
```

### PyPi Registery

`provisioner` is also available in the `PyPi` registry, and can be installed with,

```
pip install provisioner
```

### Hightlights

1. Eliminates the cumbersome process of setting up environment for learning big data tools,
2. Field tested to be stable, with appropriate error handling procedures in place for `error-discovery` while setting up the environment.
3. `cluster_config.yml` file is generated when the clusters are provisioned, with information about  `networking`, `naming`, and `web ui` addresses, for easy access.
4. Once the required clusters are provisioned, the tool automatically spins up services in the clusters, with required terminal and web-ui interfaces.
5. And its a go time!
