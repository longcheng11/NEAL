% generate input for Mininet, 10 nodes,  10GB

clc;
clear;
close all;
warning off;
addpath 'func\'

%s1 which group test
%s2 which test

for s1=1:1
    for s2=1:1
        for repeat=5
            fprintf('EXP: [%d\t%d],%d\n',s1, s2, repeat);
            Join(s1,s2,repeat);
        end
    end
end
fprintf("join is done\n")

function Join(s1, s2, repeat)

global N; % number of nodes
global P; % number of partitions
global B; % network bandwidth 1D matrix
global H; %size of partitions on each node 2D matrix

%experiment setting
vary=["node\"];
expr=[10];

%data input path
iPath_R=strcat('data\',vary(s1),int2str(expr(s1,s2)),'_R');
iPath_S=strcat('data\',vary(s1),int2str(expr(s1,s2)),'_S');
iPath_A=strcat('data\',vary(s1),int2str(expr(s1,s2)),'_A');

%---Output the matrix ------%
oPath=strcat('results\join\',vary(s1),int2str(expr(s1,s2)),'\');

%load relations and skew part
R=load(iPath_R);
S=load(iPath_S);
A=load(iPath_A);

%change #tuples into size in Byte
tuple=10; %tuple size in Byte
R=R*tuple;
S=S*tuple;
A=A*tuple;

%the number of partitions and nodes
[P,N]=size(R);

%bandwdith
B=rand(N,1)' * 1024*1024*1024/8; % in Byte/s

%save the generated bandwidth matrix
B_PATH=strcat('data\bandwidth\','bw_',int2str(s1),'_',int2str(s2),'_',int2str(repeat));
dlmwrite(B_PATH, B,'precision', '%.2f');

%the whole input
H=R+S;
%H(1,:)=H(1,:)+A;

%---data locality assignment------%
%HASH
Hash_X=mod((0:P-1)',N)+1;

%Min
[Max,Min_X]=max(H,[],2);

%---compute flow volumn matrix------%
%HASH
Hash_V=zeros(N,N);
for j=1:length(Hash_X) % for partition j
    i=Hash_X(j); % the j-th partiion is assigned to node i
    for k=1:N
        Hash_V(k,i)=Hash_V(k,i)+ H(j,k);
    end
end
Hash_V=Hash_V-Hash_V.*eye(size(Hash_V)); % self transfer set to 0, in Bytes
Hash_V_SUM=sum(Hash_V(:))/(1024*1024*1024);  %in GB
dlmwrite(strcat(oPath,"Hash_V"), Hash_V,'precision', '%i');

%Min
Min_V=zeros(N,N);
for j=1:length(Min_X)
    i=Min_X(j);
    for k=1:N
        Min_V(k,i)=Min_V(k,i)+ H(j,k);
    end
end
Min_V=Min_V-Min_V.*eye(size(Min_V));
Min_V_SUM=sum(Min_V(:))/(1024*1024*1024);
dlmwrite(strcat(oPath,"Min_V"), Min_V,'precision', '%i');

%---compute flow bandwidth matrix (Equal)------%
Hash_BE =zeros(N,N);
for i=1:N % the row number
    nz=sum(Hash_V(i,:)~=0); %non-zero numbers
    for j=1:N % the row number
        if(Hash_V(i,j)~=0)
            Hash_BE(i,j)=B(i)/nz;
        end
    end
end
dlmwrite(strcat(oPath,"Hash_BE"), Hash_BE,'precision', '%.2f');

Min_BE =zeros(N,N);
for i=1:N % the row number
    nz=sum(Min_V(i,:)~=0); %non-zero numbers
    for j=1:N % the row number
        if(Min_V(i,j)~=0)
            Min_BE(i,j)=B(i)/nz;
        end
    end
end
dlmwrite(strcat(oPath,"Min_BE"), Min_BE,'precision', '%.2f');

%---compute flow bandwidth matrix (Coflow)------%
Hash_Tau=max([sum(Hash_V,2)'./B sum(Hash_V)./B]); %the communication time
Hash_BC=Hash_V/Hash_Tau; %the bandwidth assignment for each flow
dlmwrite(strcat(oPath,"Hash_BC"), Hash_BC,'precision', '%.2f');

Min_Tau=max([sum(Min_V,2)'./B sum(Min_V)./B]);
Min_BC=Min_V/Min_Tau;
dlmwrite(strcat(oPath,"Min_BC"), Min_BC,'precision', '%.2f');

%---NEAL Computing -- three times----%
[NEAL_Tau, NL_X]=NEAL();  %get optimal time and locality assignment
[Max,NEAL_X]=max(NL_X,[],2);
NEAL_V=zeros(N,N);  %calculate flow size
for j=1:length(NEAL_X)
    i=NEAL_X(j);
    for k=1:N
        NEAL_V(k,i)=NEAL_V(k,i)+ H(j,k);
    end
end
NEAL_V=NEAL_V-NEAL_V.*eye(size(NEAL_V));
NEAL_V_SUM=sum(NEAL_V(:))/(1024*1024*1024); %in GB
NEAL_B=NEAL_V/NEAL_Tau; %the bandwidth assignment for each flow
%output
dlmwrite(strcat(oPath,"NEAL_V"), NEAL_V,'precision', '%i');
dlmwrite(strcat(oPath,"NEAL_B"), NEAL_B,'precision', '%.2f');

%print out
fprintf('%.2f\t%.2f\t%.2f\n',Hash_V_SUM ,Min_V_SUM,NEAL_V_SUM);
fprintf('%.2f\t%.2f\t%.2f\n',Hash_Tau, Min_Tau, NEAL_Tau);
end

