% fitness value calculate function
function [fobj, OUT, IN, x] = fitness(X)

global N;
global P;
global B;
global H;

X1 = zeros(P,N);
for i = 1:P
    for j = 1:N
        X1(i,j) = X(N*(i-1)+j);
    end
end

X2 = zeros(P,N);
for i = 1:P
    tmps1   = X1(i,:);
    [V,I]   = max(tmps1);
    X2(i,I) = 1;
end

%convert X to decision variable matrix x
x = zeros(P,N);
for i = 1:P
    for j = 1:N
        if X2(i,j) > 0
            x(i,j) = 1;
        else
            x(i,j) = 0;
        end
    end
end

%outflow for each node
T1=zeros(1,N);
for i = 1:N
    obj = 0;
    for j = 1:N
        if(j~=i)
            for k = 1:P
                obj = obj +H(k,i)/B(i)*x(k,j); % note that the index (k,j) of x is for x_jk, also for H
            end
        end
    end
    T1(i)=obj;
end

%inflow for each node
T2=zeros(1,N);
for j = 1:N
    obj = 0;
    for i = 1:N
        if(i~=j)
            for k = 1:P
                obj = obj +H(k,i)/B(j)*x(k,j);
            end
        end
    end
    T2(j)=obj;
end

OUT=max(T1);
IN=max(T2);

%fobj=max([T1 T2])
fobj = max(OUT,IN);
