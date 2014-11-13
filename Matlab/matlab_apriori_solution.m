% Script to do the project.
% By MCT

% Read the  data, translate into rows and columns
% will have N rows, 17 columns, one for each category
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('Processing data...')
cd ..
cd assets
f = fopen('msnbc990928.seq');
cd ..
cd Matlab

fseek(f,191,'bof'); % start at the beginning of the data file

records = [];
tic
while 1
	tline = fgets(f);
	% TLINE should be a string holding a list of the page topic numbers
	if tline == -1
		break
	end

	create_record_command = sprintf('record = [%s];', tline);
	eval(create_record_command);
	
	dataline = zeros(1,17); % expecting 17 different topics

	dataline(record) = 1;
	
	records = [records; dataline];
end
fclose(f);
save('msnbc_matlab_matrix','records')
fprintf('...Done\n')
toc
%%
% load msnbc_matlab_matrix

%% Ignore FRONTPAGE
records(:,1) = [];

%% A-PRIORI ASSOCIATION MINING
% Topic labels
% categories = {['frontpage'],['news'],['tech'],['local'],['opinion'],['on-air'],['misc'],['weather'],['msn-news'],['health'],['living'],['business'],['msn-sports'],['sports'],['summary'],['bbs'],['travel']};
categories = {['news'],['tech'],['local'],['opinion'],['on-air'],['misc'],['weather'],['msn-news'],['health'],['living'],['business'],['msn-sports'],['sports'],['summary'],['bbs'],['travel']};

fprintf('Done building data matrix\n')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Apriori mining parameters
minSup = 0.0001;
minConf = 0.5;
nRules = 20;
sortFlag = 1; % 1 sorts resulting rules by support, 2 sorts resulting rules by confidence
fname = 'mini_msn_apriori_result'; % Results will be output in a more readable form to "fname".txt

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
datestr(now)
fprintf('Running FINDRULES...')
tic
[Rules, FreqItemsets] = findRules(records, minSup, minConf, nRules, sortFlag, categories, fname);
fprintf('...Done\n')
toc
disp(['See the file named ' fname '.txt for the association rules']);

type mini_msn_apriori_result.txt
save('Apriori_results')
