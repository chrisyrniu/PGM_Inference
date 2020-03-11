import brml.*

load diseaseNet_compat_BRML-ObjectOriented.mat; 

pot_cond = pot;

% initialize the observed potentions
for i = 21:25
    a = pot{i}.table(:,:,:,:);
    a(1,:,:,:) = 1;
    a(2,:,:,:) = 0;
    pot_cond{i}.table(:,:,:,:) = a;
end

for j = 26:30
    b = pot{j}.table(:,:,:,:);
    b(2,:,:,:) = 1;
    b(1,:,:,:) = 0;
    pot_cond{j}.table(:,:,:,:) = b;
end

pot_cond=str2cell(setpotclass(pot_cond,'array'));

[jtpot jtsep infostruct]=jtree(pot_cond); % setup the Junction Tree

jtpot=absorption(jtpot,jtsep,infostruct); % do full round of absorption
% disp(jtpot);

output = zeros(1, 20); % initialize the output
yes = 1;

for disease = 1:20
    jtpotnum = whichpot(jtpot,disease,1); % find a single JT potential that contains symptom
%     disp(jtpot{1});
    margpot = sumpot(jtpot(jtpotnum),disease,0); % sum over everything but symptom
%     disp(margpot(1).table);
    output(yes, disease) = margpot.table(yes)./sum(margpot.table); % get potientials and put in the output
end 

disp(output);