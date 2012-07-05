function build_mlr_model(propertiesCSVFilePath)

data = csvread(propertiesCSVFilePath);

%read all independent variable columns
x = data(:, 2:end);

%read dependend variable values
y = data(:, 1);

%get coefficients
x1 = x(:, 1);
x2 = x(:, 2);
preparedX = [ones(size(x1)) x1 x2 x1.*x2];


