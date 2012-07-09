function build_mlr_model(propertiesCSVFilePath)

data = csvread(propertiesCSVFilePath);

%read dependend variable values
y = data(:, 1);

%read all independent variable columns
x = data(:, 2:end);

%get coefficients
x1 = x(:, 1);
x2 = x(:, 2);
x3 = x(:, 3);
x4 = x(:, 4);
x5 = x(:, 5);

%multiple linear regression
X = [ones(size(x1)) x1 x2 x3 x4 x5];
b = regress(y,X) % Removes NaN data
yPred = b(1) + b(2)*x1 + b(3)*x2 + b(4)*x3 + b(5)*x4 + b(6)*x5;

yResid = y - yPred;

SSresid = sum(yResid.^2);
SStotal = (length(y)-1) * var(y);
rsq = 1 - SSresid/SStotal

scatter(y, yPred)
