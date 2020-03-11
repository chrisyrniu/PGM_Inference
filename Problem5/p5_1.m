import brml.*

load diseaseNet_compat_BRML-ObjectOriented.mat; 

pot=str2cell(setpotclass(pot,'array')); % convert to cell array

[jtpot jtsep infostruct]=jtree(pot); % setup the Junction Tree

jtpot=absorption(jtpot,jtsep,infostruct); % do full round of absorption

output = zeros(1, 40); % initialize the output
yes = 1;

for symptom = 21:60
    jtpotnum = whichpot(jtpot,symptom,1); % find a single JT potential that contains symptom
    margpot = sumpot(jtpot(jtpotnum),symptom,0); % sum over everything but symptom
    output(yes, symptom-20) = margpot.table(yes)./sum(margpot.table); % get potientials and put in the output
end 

disp(output);