% Script to do the project.
% By MCT
% FindRules from  Narine Manukyan
% See: http://www.mathworks.com/matlabcentral/fileexchange/42541-association-rules

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
TOTAL_RECORDS = 989818;
records = zeros(TOTAL_RECORDS,17);
tic

for line = 1:TOTAL_RECORDS
	tline = fgets(f);
	% TLINE should be a string holding a list of the page topic numbers
	if tline == -1
		break
	end

	create_record_command = sprintf('record = [%s];', tline);
	eval(create_record_command);
	
    records(line,record) = 1;
    if mod(line,10000) == 0
        fprintf('Line = %d\n', line)
        toc
    end
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
nRules = 100;
sortFlag = 1; % 1 sorts resulting rules by support, 2 sorts resulting rules by confidence
fname = 'msn_apriori_result'; % Results will be output in a more readable form to "fname".txt

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('Running FINDRULES...')
tic
[Rules, FreqItemsets] = findRules(records, minSup, minConf, nRules, sortFlag, categories, fname);
fprintf('...Done\n')
toc
disp(['See the file named ' fname '.txt for the association rules']);

type msn_apriori_result.txt
save('Apriori_results')
