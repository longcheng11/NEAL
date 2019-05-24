% get the optimal solution
function [NEAL_Tau,NEAL_X] = NEAL()

global N;
global P;
global B;
global H;

%-------Algorithm Parameter-------%
Iters=50; %number of iterations
Num=10; %number of search agents

%-------WOA Implementation-------%
D = P*N; %search space
woa_idx      = zeros(1,D);
woa_get      = inf;

%initialize individuals
for i=1:Num-1
    for j=1:D
        xwoa(i,j)=randn;
    end
end

%an individual is with the hash scheduling plan
for i=Num
    for j=1:D
        if(mod(j-1,N)==mod(floor((j-1)/N),N))
            xwoa(i,j)=1;
        else
            xwoa(i,j)=0;
        end
    end
end

for t=1:Iters
    for i=1:Num
        %objective functions
        [pa(i),pa1(i),pa2(i),x] = fitness(xwoa(i,:));
        Fitout                        = pa(i);
        %update
        if Fitout < woa_get
            woa_get = Fitout;
            woa_idx = xwoa(i,:);
        end
    end
    
    c1 = 2-t*((2)/Iters);
    c2 =-1+t*((-1)/Iters);
    
    %update position of each search agent
    for i=1:Num
        r1         = rand();
        r2         = rand();
        K1         = 2*c1*r1-c1;
        K2         = 2*r2;
        l          = c2*rand + 1;
        rand_flag  = rand();
        
        if rand_flag<0.5
            if abs(K1)>=1
                RLidx    = floor(Num*rand()+1);
                X_rand   = xwoa(RLidx, :);
                D_X_rand = abs(K2*X_rand(1:D)-xwoa(i,1:D));
                xwoa(i,1:D)= X_rand(1:D)-K1*D_X_rand;
            else
                D_Leader = abs(K2*woa_idx(1:D)-xwoa(i,1:D));
                xwoa(i,1:D)= woa_idx(1:D)-K1*D_Leader;
            end
        else
            distLeader = abs(woa_idx(1:D)-xwoa(i,1:D));
            xwoa(i,1:D)  = distLeader*exp(l).*cos(l.*2*pi)+woa_idx(1:D);
        end
    end
end

[NEAL_Tau, OUT, IN, NEAL_X]  = fitness(woa_idx);
