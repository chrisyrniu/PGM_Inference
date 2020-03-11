import brml.*

load diseaseNet_compat_BRML-ObjectOriented.mat; 

pot=str2cell(setpotclass(pot,'array'));

output = zeros(1, 40); % initialize the output
yes = 1;

for symptom = 21:60
    newpot = multpots({pot{symptom} pot{pot{symptom}.variables(2)} pot{pot{symptom}.variables(3)} pot{pot{symptom}.variables(4)}}); % only multiply the potentials of the symptom and its parents
    margpot = sumpot(newpot,symptom,0);  % sum over everything but symptom
    output(yes, symptom-20) = margpot.table(yes)./sum(margpot.table); % get potientials and put in the output
end


disp(output); % the results are the same as the JTA