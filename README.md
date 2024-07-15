# ML well project

<h2>About the project</h2>
This project provide an opportunity to make a simulation in hydrodynamic models.

Main goals of the project:
    <ul>
        <li>Generate models with all possibles realizations from user data</li>
        <li>Select an optimal well construction</li>
        <li>Creating a dataset for machine learning</li>
    </ul>

<h2>Getting started</h2>

1. Clone the repo
```
git@github.com:CollapsingTime/ML_well_project.git
```

2. Copy .env.sample and setup your local paths
```
cp .env.sample .env
```

3. Run <b>create_data_files.py</b> to generate DATA

4. Create Docker image when all models are complete
```
docker build -t <image name> .
```

5. Run Docker container
```
docker run <image name>
```

After this stage you will have a dataset for ML. It's necessary for predicting the desire values based on the input parameters. In this repository, these are the gas production and runtime parameters