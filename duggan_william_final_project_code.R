# Decision Tree classification 

# Importing the dataset
dataset = read.csv('wine.csv')


# Encoding the target feature to label by cultivator 1-3
# dataset$Cultivator = factor(dataset$Class, 
                       #levels = c(1, 2, 3),
                       #labels = c('Cultivator 1', 'Cultivator 2', 'Cultivator 3'))

# Subset certain columns in dataset to 
dataset1 = dataset[, 1:3]


# Splitting dataset1 into the Training set and Test set
# install.packages('caTools')
library(caTools)
set.seed(123)# can be anything here
split = sample.split(dataset1$Cultivator, SplitRatio = 0.75)
training_set = subset(dataset1, split == TRUE)
test_set = subset(dataset1, split == FALSE)

# Feature Scaling Alcohol and Ash constituents
training_set[, 2:3] = scale(training_set[, 2:3])
test_set[, 2:3] = scale(test_set[, 2:3])

# Fitting Decision Tree classification 
# install.packages('rpart')
library(rpart)
classifier = rpart(formula = Cultivator ~ .,
                   data = training_set)

# Predicting the Test set results
y_pred = predict(classifier, newdata = test_set[, 2:3], type = 'class')

# Making the Confusion Matrix
cm = table(test_set[, 3], y_pred)

# Visualising the Training set results
library(ElemStatLearn)
set = training_set
X1 = seq(min(set[, 1]) - 1, max(set[, 1]) + 1, by = 0.01)
X2 = seq(min(set[, 2]) - 1, max(set[, 2]) + 1, by = 0.01)
grid_set = expand.grid(X1, X2)
colnames(grid_set) = c('Cultivator', 'Alcohol')
y_grid = predict(classifier, newdata = grid_set, type = 'class')
plot(set[, -3],
     main = 'Decision Tree (Train_set)',
     xlab = 'Cultivator', ylab = 'Alcohol',
     xlim = range(X1), ylim = range(X2))
contour(X1, X2, matrix(as.numeric(y_grid), length(X1), length(X2)), add = TRUE)
points(grid_set, pch = '.', col = ifelse(y_grid == 1, 'springgreen3', 'tomato'))
points(set, pch = 21, bg = ifelse(set[, 3] == 1, 'green4', 'red3'))

# Visualizing the Test set results
library(ElemStatLearn)
set = test_set
X1 = seq(min(set[, 1]) - 1, max(set[, 1]) + 1, by = 0.01)
X2 = seq(min(set[, 2]) - 1, max(set[, 2]) + 1, by = 0.01)
grid_set = expand.grid(X1, X2)
colnames(grid_set) = c('Cultivator', 'Alcohol')
y_grid = predict(classifier, newdata = grid_set, type = 'class')
plot(set[, -3], main = 'Decision Tree (Test_set)',
     xlab = 'Cultivator', ylab = 'Estimated Salary',
     xlim = range(X1), ylim = range(X2))
contour(X1, X2, matrix(as.numeric(y_grid), length(X1), length(X2)), add = TRUE)
points(grid_set, pch = '.', col = ifelse(y_grid == 1, 'springgreen3', 'tomato'))
points(set, pch = 21, bg = ifelse(set[, 3] == 1, 'green4', 'red3'))

# Visualizing Decision Tree regression
library(ggplot2)
ggplot() +
  geom_point(aes(x = dataset1$Cultivator, y = dataset1$Alcohol),
             colour = 'red') +
  geom_line(aes(x = dataset1$Cultivator, y = predict))

# Plotting the Decision Tree
plot(classifier)
text(classifier)
