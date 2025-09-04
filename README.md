
# Real-Time Prediction of Asteroid Hazard Level

This project is a machine learning–based system designed to predict whether an asteroid is potentially hazardous to Earth. It integrates NASA’s Near-Earth Object API for real-time asteroid data collection and stores the retrieved information in a MongoDB database for efficient management.

The prediction model is built using a Random Forest Classifier, achieving an impressive 97% accuracy in classifying asteroids as hazardous or non-hazardous.

Beyond hazard prediction, the system provides detailed technical insights about each asteroid, enabling both researchers and enthusiasts to explore its orbital and physical characteristics.




## Try it out 
  [Asteroid Hazard Predictor](http://ec2-16-171-115-145.eu-north-1.compute.amazonaws.com:8000/)



## Features

- A RFC Model that Predicts if the Asteroid Near earth is a Potential Hazard or Not 
    
    ```/predict```
- A Dashboard that gives the technicall information of each Asteroid , Important for further Analysis
    
    ```/visualize```
- A Method that updates the Asteroid data found the recently
  
    ```/updatedata``` 

## Screenshots

<img width="1919" height="866" alt="Screenshot 2025-09-01 230317" src="https://github.com/user-attachments/assets/563aacd0-b5f5-4ae1-9b80-b7b84bee5bf4" />

<img width="1919" height="874" alt="Screenshot 2025-09-01 230344" src="https://github.com/user-attachments/assets/f3e2510f-4bed-4e5c-a202-b96a39a961c1" />


<img width="1919" height="864" alt="Screenshot 2025-09-01 230408" src="https://github.com/user-attachments/assets/f22d87e1-40a5-49b9-bdd9-41b6547892dd" />


## Technical Fields Explained

absolute_magnitude_h → Brightness of the asteroid; lower values mean it is brighter and usually larger.

jupiter_tisserand_invariant → A value that helps classify the asteroid’s orbital dynamics relative to Jupiter.

eccentricity → Measures how much the orbit deviates from being a perfect circle (0 = circular, closer to 1 = elongated).

inclination → The tilt of the asteroid’s orbit relative to Earth’s orbital plane, measured in degrees.

ascending_node_longitude → The angle that locates where the asteroid crosses Earth’s orbital plane going north.

perihelion_distance → The asteroid’s closest distance to the Sun in its orbit.

perihelion_argument → The orientation of the orbit within its plane; specifies where perihelion occurs.

mean_anomaly → A parameter that indicates the asteroid’s position along its orbit at a specific time.

estimated_diameter_max → The maximum estimated size of the asteroid in kilometers.

relative_velocity_kmps → The asteroid’s velocity relative to Earth, measured in kilometers per second.

miss_distance_in_astronomical → How far the asteroid will pass from Earth, expressed in astronomical units (1 AU ≈ Earth-Sun distance).





## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`MONGO_DB_URL`


## Installation

Install this project with docker

```bash
docker pull parthbillore/todays-asteroid-hazard-prediction:V1
```
To Run 
```bash 
docker run -p 8080:80 --rm astro
```    
## Lessons Learned

Working with APIs – fetching and integrating real-time asteroid data from NASA’s API.

Database handling – storing and managing structured data effectively.

MongoDB – using NoSQL for flexible storage of large and evolving datasets.

Deployment – hosting the application on AWS EC2 instances for scalability.

Docker – containerizing the project for easy deployment and portability.

Working with large & complex datasets – cleaning, preprocessing, and extracting meaningful features.


## Feedback

If you have any feedback, please reach out to me at https://www.linkedin.com/in/parth-billore-9647332a1/


## Authors

- [@billoreparth](https://github.com/billoreparth)

