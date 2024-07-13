# ML well project

<h2>About the project</h2>
This project provide an opportunity to make a simulation in hydrodynamic models.

The main goal is to select an optimal way to define a well construction among all the possibles realizations.

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