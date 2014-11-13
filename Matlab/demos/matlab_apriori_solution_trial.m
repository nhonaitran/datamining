% Script to do the project.
% By MCT

% Read the  data, translate into rows and columns
% will have N rows, 17 columns, one for each category
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('Processing data...')
f = fopen('msnbc_mini.seq');
tic
fseek(f,186,'bof'); % skip to the beginning of the data file

records = [];

while 1
	tline = fgets(f);
	% TLINE should be a string holding a list of the page topic numbers
	if tline == -1
		break
	end
	%fprintf('____________________________________________\n')
	%fprintf('Line:* %s *\n', tline)

	create_record_command = sprintf('record = [%s];', tline);
	eval(create_record_command);
	
	dataline = zeros(1,17); % expecting 17 different topics

	dataline(record) = 1;
	
	%for element = record % for each element in record...
	%	dataline(element) = 1;
	%end
	%dataline
	records = [records; dataline];
end
fclose(f);
fprintf('...Done\n')
toc
pause(1)
% Topic labels
categories = {['frontpage'],['news'],['tech'],['local'],['opinion'],['on-air'],['misc'],['weather'],['msn-news'],['health'],['living'],['business'],['msn-sports'],['sports'],['summary'],['bbs'],['travel']};

fprintf('Done building data matrix\n')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Apriori mining parameters
minSup = 0.2;
minConf = 0.5;
nRules = 100;
sortFlag = 2; % 1 sorts resulting rules by support, 2 sorts resulting rules by confidence
fname = 'mini_msn_apriori_result'; % Results will be output in a more readable form to "fname".txt

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('Running FINDRULES...')
tic
[Rules FreqItemsets] = findRules(records, minSup, minConf, nRules, sortFlag, categories, fname);
fprintf('...Done\n')
toc
disp(['See the file named ' fname '.txt for the association rules']);

type mini_msn_apriori_result.txt
