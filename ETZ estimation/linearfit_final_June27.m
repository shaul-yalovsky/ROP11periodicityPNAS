clear all;
close all;
clc


A=dlmread('rop111_ABA.txt');
x=A(:,1);
y=A(:,2);
Nx = size(x);


indices = find(x==1);
Nindices = length(indices);


for j=1:Nindices
    start_x = indices(j)+20;
    if j == Nindices,
        end_x = Nx;
    else
        end_x = indices(j+1)-1;
    end

    x1 = x(start_x:end_x);
    yy = y(start_x:end_x);
    ix = find(yy <= 0);
    yy(ix) = [];
    x1(ix) = [];
    y1 = log(yy);
    



    N1 = size(x1);


    p = polyfit(x1,y1,1);

    figure(j);
    plot(x1,(y1),'.');hold on;
    plot(x1, p(1)*x1+p(2),'r');



    a = p(1);
    b = -1;
    c = p(2);

    dist_vec = zeros(N1);
    for i=1:N1
        xx = x1(i);
        yy = y1(i);
        dist_vec(i) = abs(a*xx+b*yy+c)/(sqrt(a^2+b^2));
    end    

    [C,ix] = max(dist_vec);


    x0 = x1(ix);
    y0 = y1(ix);





    xz = (x0+p(1)*y0-p(1)*p(2))/(1+p(1)^2);
    yz = (p(1)*x0+p(1)^2*y0+p(2))/(1+p(1)^2);





    hold on; 
    plot(x0,y0,'go','markersize',12);
    hold on;
    plot([x0,xz],[y0,yz],'m');
    t = sprintf('dist=%.2f',C);
    axis equal;
    title(t);
end











