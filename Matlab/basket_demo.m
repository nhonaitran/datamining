% This is the Association rule example from the book

minSup = 0.35;
minConf = 0.7;
nRules = 100;
sortFlag = 1; % 1 sorts resulting rules by support, 2 sorts resulting rules by confidence
fname = 'basket_demo'; % Results will be output in a more readable form to "fname".txt
labels = {['Bread'],['Milk'],['Diapers'],['Beer'],['Eggs'],['Cola']};

% See Table 6.2, page 329
transactions = [1 1 0 0 0 0; 1 0 1 1 1 0; 0 1 1 1 0 1; 1 1 1 1 0 0; 1 1 1 0 0 1];

[Rules FreqItemsets] = findRules(transactions, minSup, minConf, nRules, sortFlag, labels, fname);
disp(['See the file named ' fname '.txt for the association rules']);

type basket_demo.txt

