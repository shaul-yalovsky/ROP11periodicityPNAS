MyData1=load("Log rearrangement\DMSO.txt")
MyData2=load("Log rearrangement\Oryzalin.txt")


plot(MyData1(:,1),MyData1(:,2), 'LineWidth', 4)
hold on
plot(MyData2(:,1),MyData2(:,2), 'LineWidth', 4)
hold on

%title ('Smoothed amplitude spectra mock kappa 0.1');
xlabel ('k(1/micron)');
ylabel ('F(k)');
legend ('mock', 'Oryzalin')