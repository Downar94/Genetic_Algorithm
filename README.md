# Genetic_Algorithm
- Description
- Results

## Description
Genetic Algorithm is one of the evolutionary algorithms. This kind of algorithm allows to resolve many problems thanks to the evolutionary model with different modifications during the stages of the life cycle. For my purpose i have used the genetic algorithm for resolving salesman travelling problem. Genetic algorithms are searching the large space of solutions and choosing the best one. As you can see on the graph <...>, the best solution is only the local best solution, not the global one. In my case the quality of the best local solution depends of the number of algorithm's iterations. The genetic algorithm that i have implemented consists of the following steps:
1. Set algorithm parameters such as mutation rate, iteration number, chromosome number, city list (only for the salesman travelling problem).
2. Generate population - the population consists of the chromosomes created by sampling the city list. Each gene in the chromosome is the number of the city from the list, each individual chromosome contains information about sequence of the visited cities.
![im1](https://user-images.githubusercontent.com/44844566/196499983-5cbef323-6933-4cc1-baad-14ae90842309.PNG)
3. Create the selection ranking according to the fitness function. In my case fitness function is based on the reverse total distance in individual chromosome.
![im2](https://user-images.githubusercontent.com/44844566/196499999-f4bb6e0b-dc32-4a3e-af15-a7fdb7b75cc8.PNG)
4. Select potential parents according to the selection model. In my algorithm I have used steady state model, where the 80% of the current population goes to the next population and 20% is replaced. The individuals from the current population by keeping 10% from the current population with the highest rank and choosing the rest using the roulette method. These parents are chosen taking into account probability factor, according to their ranking.
![im3](https://user-images.githubusercontent.com/44844566/196500000-fa00207d-988c-4bf0-8593-daf5d96ff032.PNG)
5. Create children by crossovering the potential parents. A child's chromosome is made up using half of the genes of one parent and using half of the genes of the other parent.
![im4](https://user-images.githubusercontent.com/44844566/196499996-cc659e8e-53c2-41ea-9852-06d577914c60.PNG)
6. Mutate children by replacing 2 randomly chosen genes in the chromosome.
![im5](https://user-images.githubusercontent.com/44844566/196499997-74773324-3488-487b-a3b9-fd2c1e22af15.PNG)
7. Create next population which consists of the potential parents and the children.
![im6](https://user-images.githubusercontent.com/44844566/196499998-b94fc7cb-674d-4074-a05a-9fc77e03f536.PNG)
8. Repeat steps 4-7 for a given number of iterations. 
9. Choose the chromosome with the best ranking from the final population - it is our best local solution.
## Results
### Final shortest path:
![result](https://user-images.githubusercontent.com/44844566/194939635-897acc2e-f3e7-44d4-b02e-7f8d71a981d6.gif)
### Line graph:
![graph](https://user-images.githubusercontent.com/44844566/194936476-f954aada-0f30-40ab-be00-d6c66f50de18.PNG)
