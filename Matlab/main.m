clc;
clear;
close all;
warning off;
addpath 'func\'

%s1 which group test
%s2 which test

for s1=1:3
    for s2=1:4
        for repeat=1:5
            fprintf('EXP: [%d\t%d],%d\n',s1, s2, repeat);
            Join(s1,s2,repeat);
        end
    end
end

fprintf("join is done\n")