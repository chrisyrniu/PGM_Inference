trans = zeros(83, 83);

% state c1 and c2, self transition
trans(82,82) = 0.8;
trans(83,83) = 0.8;
% state c1 transfers to random first name
pos_s1 = [1, 6, 11, 15, 18];
for i = pos_s1
    trans(82, i) = 0.2/5;
end
% state c2 transfers to random last name
pos_s2 = [23, 29, 35, 38, 43, 54, 65];
for j = pos_s2
    trans(83, j) = 0.2/7;
end
% the transitions in the same word
for k = [1:4 6:9 11:13 15:16 18:21 23:27 29:33 35:36 38:41 43:52 54:63 65:80]
    trans(k, k+1) = 1;
end
% first name transfer to state c2
pos_to_s2 = [5, 10, 14, 17, 22];
for m = pos_to_s2
    trans(m, 83) = 1;
end
% last name transfer to state c1
pos_to_s1 = [28, 34, 37, 42, 53, 64, 81];
for n = pos_to_s1
    trans(n, 82) = 1;
end

% to add prior, expand the trans matrix
prior1 = zeros(83,1);
prior2 = zeros(1,84);
trans = [prior1, trans];
trans = [prior2; trans];
% set prior state as c1
trans(1,83) = 1;

emis = zeros(84, 26);
% emissions: state c1 and c2 to each character
emis(83:84, :) = 1/26;
% emissions: state 2-82 to each character
emis(2:82, :) = 0.7/25;
c_index = [4,1,22,9,4,1,14,20,15,14,6,18,5,4,10,9,13,2,1,18,18,25,2,1,18,2,5,18,9,12,19,21,14,7,6,15,24,3,8,1,9,14,6,9,20,26,23,9,12,12,9,1,13,17,21,9,14,3,5,1,4,1,13,19,7,18,1,6,22,15,14,21,14,20,5,18,8,15,19,5,14];
for l = 2:82
    emis(l, c_index(l-1)) = 0.3;
end

seq = cell2mat(struct2cell(load('noisystring.mat')));
% get the optimal state squence through viterbi
estimatedStates = hmmviterbi(seq,trans,emis, 'Symbols', ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']);
% eliminate state 1 and 2 in the sequence
extracted = [];
for state = estimatedStates
    if state==2||state==7||state==12||state==16||state==19||state==24||state==30||state==36||state==39||state==44||state==55||state==66
        extracted(end+1) = state;
    end
end

% generate the output matrix
output = zeros(5,7);
length = fix(size(extracted)/2);

for p = 1:length(1,2)
    switch extracted(2*p-1)
        case 2
            i1 = 1;
        case 7
            i1 = 2;
        case 12
            i1 = 3;
        case 16
            i1 = 4;
        case 19 
            i1 = 5;
    end
            
    switch extracted(2*p)
        case 24
            i2 = 1;
        case 30
            i2 = 2;
        case 36
            i2 = 3;
        case 39
            i2 = 4;
        case 44
            i2 = 5;
        case 55
            i2 = 6;
        case 66
            i2 = 7;
    end       
    output(i1, i2) = output(i1, i2) + 1;
end

disp(output);
disp(estimatedStates(9961:10000));
disp(seq(9961:10000));
                
    
    
        

