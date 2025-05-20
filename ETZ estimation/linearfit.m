clear all;
close all;
clc


A=dlmread('Col-0_mock.txt');
x=A(:,1);
y=A(:,2);
N = size(x);

%figure(1);
%plot(x,log(y), '.');
%title('whole data');

x1 = x(1+20:50);
y1 = log(y(1+20:50));
%x1 = x1-x1(1);

N1 = size(x1);


p = polyfit(x1,y1,1);

figure(2);
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

%xz = (b*(b*x0-a*y0)-a*c)/(a^2+b^2);
%yz = (a*(-b*x0+a*y0)-b*c)/(a^2+b^2);



xz = (x0+p(1)*y0-p(1)*p(2))/(1+p(1)^2);
yz = (p(1)*x0+p(1)^2*y0+p(2))/(1+p(1)^2);


% a1 = -1/p(1);
% b1 = y0-a1*x0;
% 
% xz = (p(2)-b1)/(a1-p(1));
% yz = a1*xz+b1;


hold on; 
plot(x0,y0,'go','markersize',12);
hold on;
plot([x0,xz],[y0,yz],'m');
t = sprintf('dist=%.2f',C);
axis equal;
title(t);
%ylim([-2,8]);











