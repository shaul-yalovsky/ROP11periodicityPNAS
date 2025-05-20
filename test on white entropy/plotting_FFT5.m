% MyRAW1=load('WT_Mock/biostat Values1_smooth_fft/RAWSMOOTHED.txt')
% MySM1=load('WT_Mock/biostat Values1_smooth_fft/SMOOTHED.txt')
% MyVals1=load('WT_Mock/biostat Values1_smooth_fft/Values1.txt')
% 
% MyRAW1
% MySM1
% % MyVals1
% 
% plot(MyRAW1(:,1),MyRAW1(:,2))
% hold on
% plot(MySM1(:,1),MySM1(:,2))
% plot(MyVals1(:,1),MyVals1(:,2))

% MyRAW2=load('WT_Mock/biostat Values2_smooth_fft/RAWSMOOTHED.txt')
% MySM2=load('WT_Mock/biostat Values2_smooth_fft/SMOOTHED.txt')
% MyVals2=load('WT_Mock/biostat Values2_smooth_fft/Values2.txt')
% 
% MyRAW2
% MySM2
% MyVals2
% 
% % plot(MyRAW2(:,1),MyRAW2(:,2))
% % hold on
% % plot(MySM2(:,1),MySM2(:,2))
% plot(MyVals2(:,1),MyVals2(:,2))

% MyRAW3=load('WT_Mock/biostat Values3_smooth_fft/RAWSMOOTHED.txt')
% MySM3=load('WT_Mock/biostat Values3_smooth_fft/SMOOTHED.txt')
% 
% MyRAW3
% MySM3
% 
% plot(MyRAW3(:,1),MyRAW3(:,2))
% hold on
% plot(MySM3(:,1),MySM3(:,2))
% 
% MyRAW4=load('WT_Mock/biostat Values4_smooth_fft/RAWSMOOTHED.txt')
% MySM4=load('WT_Mock/biostat Values4_smooth_fft/SMOOTHED.txt')
% 
% MyRAW4
% MySM4
% 
% plot(MyRAW4(:,1),MyRAW4(:,2))
% hold on
% plot(MySM4(:,1),MySM4(:,2))

%MyRAWall=load('RAWSMOOTHED_all_fft_col0_mandi_kappa_0.0005.txt')
%MyRAWall=load('../Values1.txt')
%MySMall=load('SMOOTHED_all_fft_col0_mandi_kappa_0.0005.txt')
MySMall=load('SMOOTHED_WHITE_kappa_0.01.txt')
MyRAWall=load('RAWSMOOTHED_WHITE_kappa_0.01.txt')
%MySMall2=load('Col-0 WT mock EtOH/SMOOTHED_mock_kappa_0.05.txt')
%MyRAWall2=load('Col-0 WT mock EtOH/RAWSMOOTHED_mock_kappa_0.05.txt')
%MyRAWall2=load('../Values1_mock.txt')

MyRAWall
%MyRAWall2
MySMall
%MySMall2
plot(MyRAWall(:,1),MyRAWall(:,3), '.')
hold on
plot(MySMall(:,1),MySMall(:,3), 'LineWidth', 4)
hold on
plot(MySMall(:,1),MySMall(:,3)+MySMall(:,4), 'Linewidth', 1)
hold on
plot(MySMall(:,1),MySMall(:,3)-MySMall(:,4), 'Linewidth', 1)
hold on
plot(MySMall(:,1),MySMall(:,3)+MySMall(:,5), 'Linewidth', 1)
hold on
plot(MySMall(:,1),MySMall(:,3)-MySMall(:,5), 'Linewidth', 1)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% plot(MyRAWall2(:,1),MyRAWall2(:,3), '.','Color',"green")
% hold on
% xlabel ('ω');
% ylabel ('|F(ω)|');
% title ('Smoothed power spectra');
% plot(MySMall(:,1),MySMall(:,3), 'LineWidth',4,'Color','blue')
% hold on
% plot(MySMall(:,1),MySMall(:,3)+MySMall(:,4), 'LineWidth',1,'Color','blue')
% hold on
% plot(MySMall(:,1),MySMall(:,3)-MySMall(:,4), 'LineWidth',1,'Color','blue')
% hold on
% plot(MySMall2(:,1),MySMall2(:,3), 'LineWidth',4,'Color','red')
% hold on
% plot(MySMall2(:,1),MySMall2(:,3)+MySMall2(:,4), 'LineWidth',1,'Color','red')
% hold on
% plot(MySMall2(:,1),MySMall2(:,3)-MySMall2(:,4), 'LineWidth',1,'Color','red')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PSSM1=load('Col-0 1ABA/PEAK_STAT_SMOOTH_SMOOTHED_mock_kappa_0.05.txt')
% PSSM2=load('Col-0 WT mock EtOH/PEAK_STAT_SMOOTH_SMOOTHED_mock_kappa_0.05.txt')
% PS1=load('PEAK_STAT_1_SMOOTHED_mock_kappa_0.05.txt')
% PS2=load('PEAK_STAT_2_SMOOTHED_mock_kappa_0.05.txt')
% PS3=load('PEAK_STAT_3_SMOOTHED_mock_kappa_0.05.txt')
% PS4=load('PEAK_STAT_4_SMOOTHED_mock_kappa_0.05.txt')
% PS5=load('PEAK_STAT_5_SMOOTHED_mock_kappa_0.05.txt')
% PS6=load('PEAK_STAT_6_SMOOTHED_mock_kappa_0.05.txt')
% PS7=load('PEAK_STAT_7_SMOOTHED_mock_kappa_0.05.txt')
% PS8=load('PEAK_STAT_8_SMOOTHED_mock_kappa_0.05.txt')
% PS9=load('PEAK_STAT_9_SMOOTHED_mock_kappa_0.05.txt')
% PS10=load('PEAK_STAT_10_SMOOTHED_mock_kappa_0.05.txt')
% PS11=load('PEAK_STAT_11_SMOOTHED_mock_kappa_0.05.txt')
% PS12=load('PEAK_STAT_12_SMOOTHED_mock_kappa_0.05.txt')
% PS13=load('PEAK_STAT_13_SMOOTHED_mock_kappa_0.05.txt')
% PS14=load('PEAK_STAT_14_SMOOTHED_mock_kappa_0.05.txt')
% PS15=load('PEAK_STAT_15_SMOOTHED_mock_kappa_0.05.txt')
% PS16=load('PEAK_STAT_16_SMOOTHED_mock_kappa_0.05.txt')
% PS17=load('PEAK_STAT_17_SMOOTHED_mock_kappa_0.05.txt')
% PS18=load('PEAK_STAT_18_SMOOTHED_mock_kappa_0.05.txt')
% 
% plot(PS1(:,1),PS1(:,2), '.')
% hold on
% plot(PS2(:,1),PS2(:,2), '.')
% hold on
% plot(PS3(:,1),PS3(:,2), '.')
% hold on
% plot(PS4(:,1),PS4(:,2), '.')
% hold on
% plot(PS5(:,1),PS5(:,2), '.')
% hold on
% plot(PS6(:,1),PS6(:,2), '.')
% hold on
% plot(PS7(:,1),PS7(:,2), '.')
% hold on
% plot(PS8(:,1),PS8(:,2), '.')
% hold on
% plot(PS9(:,1),PS9(:,2), '.')
% hold on
% plot(PS10(:,1),PS10(:,2), '.')
% hold on
% plot(PS11(:,1),PS11(:,2), '.')
% hold on
% plot(PS12(:,1),PS12(:,2), '.')
% hold on
% plot(PS13(:,1),PS13(:,2), '.')
% hold on
% plot(PS14(:,1),PS14(:,2), '.')
% hold on
% plot(PS15(:,1),PS15(:,2), '.')
% hold on
% plot(PS16(:,1),PS16(:,2), '.')
% hold on
% plot(PS17(:,1),PS17(:,2), '.')
% hold on
% plot(PS18(:,1),PS18(:,2), '.')
% hold on
% plot(PSSM1(:,1),PSSM1(:,2), 'LineWidth',4,'color','blue')
% hold on
% plot(PSSM1(:,1),PSSM1(:,2)+PSSM1(:,3), 'LineWidth',1,'color','blue')
%hold on
%plot(PSSM1(:,1),PSSM1(:,2)-PSSM1(:,3), 'LineWidth',1,'color','blue')
%hold on
%plot(PSSM2(:,1),PSSM2(:,2), 'LineWidth',4,'color','red')
%hold on
%plot(PSSM2(:,1),PSSM2(:,2)+PSSM2(:,3), 'LineWidth',1,'color','red')
%hold on
%plot(PSSM2(:,1),PSSM2(:,2)-PSSM2(:,3), 'LineWidth',1,'color','red')

xlabel ('Frequency');
ylabel ('Amplitude');
%title ('Smoothed amplitude spectra Col-0 WT kappa 0.05');
%legend ('1uM ABA', 'variation','mock', 'variation')

%set(gca,'yscale','log');
%xlim([0 10]);
%ylim([0 1.2]);