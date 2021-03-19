# -*- coding: utf-8 -*-
"""
%   program used to plot meteor activity of meteor showers and background
%   activity from observations of BRAMS stations.
%
%   both number activities (number of meteor per hour) and duration
%   activities (total duration of meteors observed per hour = 'sum of horizontal size
%   of each rectangle') are plotted
%
%   You can choose the minimal duration of meteors: num2str(TimeLength,'%2i') typically 0
%   (all meteors) or 10s.
%
%   BACKGROUND:
%       - mean of individual days (standard deviation calc for the weight)
%       - sine fit of mean / weighted sine fit of mean (weight = 1/std^2)
%       - limitation of the weight to avoid overweights = median_weight +
%         threshold*mad_weight. Threshold is set to 10 by default. You can
%         change it.
%       - each weight over this limitation is set to it
%
%   ACTIVITY:
%       - difference between total number and background (sine fit and
%      weighted sine fit)
%       - negative velues are set to 0
%
%   Plots are stored in the directory corresponding to the meteor shower in
%   png format and in fig format.
%
%   FOR NEW SHOWER:
%       - add the csv file in the directory InputFiles
%       - modify the script:
%           . in the "SELECT CSV FILE" section, add the name of the new csv
%             file,
%           . in the "SHOWER PARAMETERS" section, adapt shower day, shower
%             month and background month if it is necessary
%
%                                               Authors: C. Tétard, H. Lamy

Created on Sat Sep  5 15:26:58 2020

@author: stijnc (rewritten from Matlab to Python 3)
"""

saveFig = 1 # 0 figures are not saved - 1 figures are saved

# choose X axis for shower activities plot:
# if Xaxis = 0 : plot as a function of time
# if Xaxis = 1 : plot as a function of solar longitude

Xaxis = 0

# duree min du meteore 0 ou 10s
TimeLength = 0

# time_res is there to convert the pixels measurements of the rectangles
# into seconds. This assumes that the file is 300 seconds long which is a
# very reasonable assumption
ffts = 16384
overlap = 14488
fs = 5512.5
time_res = round((300*fs-overlap)/(ffts-overlap))/300

# *************************************************************************
#           SELECT CSV FILE (add new file for new shower)
# *************************************************************************

shower_name = 'zetaPerseids'
shower_year = '2019'
fln_station = 'BEHUMA'
creation_date_csv = '20200602'
fln = shower_name + shower_year + '_' + fln_station + '_aggregated-' + creation_date_csv + '.csv'

# *************************************************************************
#           OPEN CSV FILE
#
# *************************************************************************

fln = 'output/aggregated/' + fln
fid = open(fln,'r')

# *************************************************************************
#           SHOWER PARAMETERS
# *************************************************************************

background_year = float(shower_year) # except quadrantids: shower_year=background_year+1;

# shower day and month, background month and year (when different from
# shower year), Right Ascension and declination of the radiant.
# TO BE ADAPTED FOR EACH NEW SHOWER

if shower_name == 'Geminids':
   shower_day   = [13, 14, 15]
   shower_month = 12
   background_month = 12
   AD  = 112
   dec = 33
elif shower_name == 'Quadrantids':
   shower_month = 1
   if shower_year == '2017':
      shower_day = [2, 3, 4]
      if fln_station == 'BEHUMA':
         background_month = [1, 12]
         background_year = [2017, 2016]
      else:
         background_month = 12
         background_year = 2016
   elif shower_year == '2018':
      shower_day = [3, 4]
      background_month = 12
      background_year = 2017
   else:
      shower_day = [3, 4, 5]
      background_month = 1
      background_year = 2019
   AD = 230
   dec = 49
elif shower_name == 'Lyrids':
   shower_day   = [22, 23, 24]
   shower_month = 4
   background_month = 4
   AD = 271
   dec = 34
elif shower_name == 'Alpha Monocerotids':
   shower_day = 22
   shower_month = 11
   background_month = 11
   AD = 117
   dec = 1
elif shower_name == 'Draconids':
   shower_day = [7, 8, 9]
   shower_month = 10
   background_month = 10
   AD = 263
   dec = 56
elif shower_name ==  'Orionids':
   shower_day = [19, 20, 21, 22]
   shower_month = 10
   background_month = 10
   AD = 95
   dec = 16
elif shower_name == 'zetaPerseids':
   shower_day = [6, 7, 8, 9, 10]
   shower_month = 6
   background_month = 6
   AD = 62
   dec = 23

# *************************************************************************
#           STATIONS PARAMETERS for radiant elevation as a function of time
# *************************************************************************

if fln_station == 'BEHUMA':
   lat = 50.192448
   lon = 5.25508;
elif fln_station == 'BEUCCL':
   lat = 50.797554
   lon = 4.35683
elif fln_station == 'BEHOVE':
   lat = 51.145058
   lon = 4.464942
elif fln_station == 'BEOPHA':
   lat = 50.657077
   lon = 4.3482255
elif fln_station == 'BEOTTI':
   lat = 50.667291
   lon = 4.579706
elif fln_station == 'BEOVER':
   lat = 51.204106
   lon = 5.432079
elif fln_station == 'BENEUF':
   lat = 49.815163
   lon = 5.399523
elif fln_station == 'BEGRIM':
   lat = 50.935643
   lon = 4.369029
elif fln_station == 'BEHAAC':
   lat = 50.974238
   lon = 4.630802
elif fln_station == 'BEGENT':
   lat = 51.023194
   lon = 3.710111
elif fln_station == 'BETINT':
   lat = 49.683219
   lon = 5.520249
elif fln_station == 'BEKAMP':
   lat = 50.950344
   lon = 4.59434

# *************************************************************************
#           READ CSV ACTIVITY FILE
# *************************************************************************
#formatCSV = '%s%s%s%s%s%s%s%f%f%f%f%s%s%s%s%s'
#A=textscan(fid,'%s%s%s%s%s%s%s%f%f%f%f%s%s%s%s%s%f','headerlines',1,'delimiter',',');
#
#nb = size(A{1},1);
#
#day      = zeros(nb,1);
#month    = day;
#year     = day;
#hh       = day;
#mm       = day;
#beg      = day;
#fin      = day;
#
#for i=1:nb
#    day(i)   = str2double(A{1}{i}(18:19));
#    month(i) = str2double(A{1}{i}(16:17));
#    year(i)  = str2double(A{1}{i}(12:15));
#    hh(i)    = str2double(A{1}{i}(21:22));
#    mm(i)    = str2double(A{1}{i}(23:24));
#    beg(i)   = A{9}(i)/time_res;
#    fin(i)   = A{11}(i)/time_res;
#end


import csv
csv_reader = csv.reader(fid)

day, month, year, hh, mm, beg, fin = [], [], [], [], [], [], []
next(csv_reader) # first row is the header
for row in csv_reader:
    day.append(row[0][18:19])
    month.append(row[0][16:17])
    year.append(row[0][12:15])
    hh.append(row[0][21:22])
    mm.append(row[0][23:24])
    beg.append(float(row[8])/time_res)
    fin.append(float(row[10])/time_res)

duration = fin-beg;

import numpy as np

day = np.array(day)
background_day = np.unique(day)
temp = np.isin(background_day,shower_day) #tbc (maybe switch parameters -- https://numpy.org/doc/stable/reference/generated/numpy.isin.html)
background_day = background_day(~temp);

nb_shower_day     = np.size(shower_day);
nb_background_day = np.size(background_day);    


# *************************************************************************
#           SOLAR LONGITUDE CSV FILE
# *************************************************************************

fln_SolarLong = 'input/SolarLongitude/' + shower_name + shower_year + '_SolarLongitude.csv'

try:
   fid_SolarLong = fopen(fln_SolarLong);
   csv_reader = csv.reader(fid_SolarLong)
   next(csv_reader)   
   SolarLongitude = zeros(1,nb_shower_day*24);

   for i in range(nb_shower_day):
       for j in range(24):
           ii = 2*j+1
           SolarLongitude(1,j+(i-1)*24) = SolarLong_csv{ii}(i) #TBD!!
except IOError:
   os.exit('the solar longitude file not generated')




# *************************************************************************
#               BAD ZOO CORRECTIONS
# *************************************************************************
#corr_badzoo = ones(24,nb_background_day);
#path_badzoo = strcat('/data/incoming/brams/ZOO_BAD/',fln_station,'/');
#
#for i=1:nb_background_day
#    for j=0:23
#        temp2 = strcat('*_',shower_year,num2str(background_month,'%02i'),...
#            num2str(background_day(i)),'_',num2str(j,'%02i'),'*');
#        temp3 = strcat(path_badzoo,temp2);
#        list_badzoo = dir(temp3);
#        if numel(list_badzoo)~=12
#            corr_badzoo(j+1,i) = 12/(12-numel(list_badzoo));
#        else
#            warning(strcat('no background data for',temp3))
#        end
#    end
#end
#
#
# *************************************************************************
#
#time1 = (0.5:23.5)';
#time2 = 0.5:nb_shower_day*24;
#
#bg_duration = zeros(24,nb_background_day);
#bg_number   = bg_duration;
#
# *************************************************************************
#           BACKGROUND
# *************************************************************************
#background_month = repmat(background_month,1,nb_background_day);
#background_year  = repmat(background_year,1,nb_background_day);
#
#for i=1:nb_background_day
#    for j=0:23
#        jk = j+1;
#        L = find(day == background_day(i) & month == background_month(i) & ...
#            year == background_year(i) & hh == j  & duration>TimeLength );
#        bg_duration(jk,i) = sum(duration(L));
#        bg_number(jk,i)   = numel(L);
#    end
#end
#
#% zoo_bad
#bg_duration = bg_duration.*corr_badzoo;
#bg_number   = bg_number.*corr_badzoo;
#
#% *************************************************************************
#%           BACKGROUND AVERAGE, STD and Weight for individual and number
#%               means and std are computed with non zero elements
#% *************************************************************************
#
#bg_number_mean   = zeros(24,1);
#bg_number_std    = bg_number_mean;
#bg_duration_mean = bg_number_mean;
#bg_duration_std  = bg_number_mean;
#
#for i=1:24
#    if numel(nonzeros(bg_number(i,:)))== 0
#        bg_number_mean(i,1) = 0;
#        bg_number_std(i,1)  = 0;
#    else
#        bg_number_mean(i,1)   = mean(nonzeros(bg_number(i,:)));
#        bg_number_std(i,1)    = std(nonzeros(bg_number(i,:)),1);
#    end
#
#    if numel(nonzeros(bg_duration(i,:))) == 0
#        bg_duration_mean(i,1) = 0;
#        bg_duration_std(i,1)  = 0;
#    else
#        bg_duration_mean(i,1) = mean(nonzeros(bg_duration(i,:)));
#        bg_duration_std(i,1)  = std(nonzeros(bg_duration(i,:)),1);
#    end
#end
#
#
#bg_number_mean_rep   = repmat(bg_number_mean,nb_shower_day,1);
#bg_duration_mean_rep = repmat(bg_duration_mean,nb_shower_day,1);
#
#% weight limitation
#if nb_background_day>1
#    bg_number_std(bg_number_std==0)=min(bg_number_std(bg_number_std>0));
#    bg_weight     = 1./bg_number_std.^2;
#    median_weight = median(bg_weight);
#    mad_weight    = mad(bg_weight,1);
#    threshold = 10;
#    limit_number_weight = median_weight + threshold*mad_weight;
#    bg_weight2 = bg_weight;
#    bg_weight2(bg_weight2>limit_number_weight) = limit_number_weight;
#else
#    bg_weight2 = ones(24,1);
#end
#
#
#% *************************************************************************
#%        SINE FIT and WEIGHTED SINE FIT
#% *************************************************************************
#%0
#%  Number sine fit
#
#    a0 = mean(bg_number_mean);
#    b0 = 0.5*(max(bg_number_mean)-min(bg_number_mean));
#    c0 = 24;
#    d0 = 0;
#    f1 = fitoptions('Method','NonLinearLeastSquare','StartPoint',[a0 b0 c0 d0]);
#    f1.algorithm = 'Levenberg-Marquardt';
#    ft1 = fittype('a+b*sin(2*pi*x/c+d)','options',f1);
#    Yfit = fit(time2',bg_number_mean_rep,ft1);
#    bg_number_mean_sinefit = Yfit.a+Yfit.b*sin(2*pi*time2/Yfit.c+Yfit.d);
#
#%  Number weighted sine fit
#
#    f1.weight = repmat(bg_weight2,nb_shower_day,1);
#    ft1 = fittype('a+b*sin(2*pi*x/c+d)','options',f1);
#    Yfit1 = fit(time2',bg_number_mean_rep,ft1);
#    bg_number_mean_weightedsinefit = Yfit1.a+Yfit1.b*sin(2*pi*time2/Yfit1.c+Yfit1.d);
#
#%  Duration sine fit
#
#    a0 = mean(bg_duration_mean);
#    b0 = 0.5*(max(bg_duration_mean)-min(bg_duration_mean));
#    c0 = 24;
#    d0 = 0;
#    f2 = fitoptions('Method','NonLinearLeastSquare','StartPoint',[a0 b0 c0 d0]);
#    f2.algorithm = 'Levenberg-Marquardt';
#    ft2 = fittype('a+b*sin(2*pi*x/c+d)','options',f2);
#    Yfit2 = fit(time2',bg_duration_mean_rep,ft2);
#    bg_duration_mean_sinefit = Yfit2.a+Yfit2.b*sin(2*pi*time2/Yfit2.c+Yfit2.d);
#
#%  Duration weighted sine fit
#    f2.weight = repmat(bg_weight2,nb_shower_day,1);
#    ft2 = fittype('a+b*sin(2*pi*x/c+d)','options',f2);
#    Yfit3 = fit(time2',bg_duration_mean_rep,ft2);
#    bg_duration_mean_weightedsinefit = Yfit3.a+Yfit3.b*sin(2*pi*time2/Yfit3.c+Yfit3.d);
#
#
#
#% *************************************************************************
#%        SHOWER ACTIVITY
#% *************************************************************************
#
#total_meteor_duration = zeros(24,nb_shower_day);
#total_meteor_number   = total_meteor_duration;
#
#for i=1:nb_shower_day
#    for j=0:23
#        jk = j+1;
#        L = find(day == shower_day(i) & month == shower_month & hh == j & duration>TimeLength );
#        total_meteor_duration(jk,i) = sum(duration(L));
#        total_meteor_number(jk,i) = sum(numel(L));
#    end
#end
#
#total_meteor_duration = reshape(total_meteor_duration,nb_shower_day*24,1);
#total_meteor_number   = reshape(total_meteor_number,nb_shower_day*24,1);
#
#shower_number  = total_meteor_number - bg_number_mean_sinefit';
#shower_numberW = total_meteor_number - bg_number_mean_weightedsinefit';
#
#shower_duration  = total_meteor_duration - bg_duration_mean_sinefit';
#shower_durationW = total_meteor_duration - bg_duration_mean_weightedsinefit';
#
#% put 0 instead of negative values;
#shower_number(shower_number<0)=0;
#shower_numberW(shower_numberW<0)=0;
#
#shower_duration(shower_duration<0)=0;
#shower_durationW(shower_durationW<0)=0;
#
#% *************************************************************************
#%        RADIANT ELEVATION
#% *************************************************************************
#
#elevation = zeros(nb_shower_day*24,1);
#
#    for i=1:nb_shower_day
#        for j=0:23
#            idate=[str2double(shower_year),shower_month,shower_day(i),j,0,0];
#            [~,ele]=EquaToHoriCoord(AD,dec,idate,lat,lon);
#            im = (i-1)*24+j+1;
#            elevation(im)=ele;
#        end
#    end
#
#
#% *************************************************************************
#%        PLOT
#% *************************************************************************
#
#% **************************
#%   BACKGROUND ACTIVITY
#% **************************
#fs = 11;    % fontsize of label
#    % data from indiv days + average and error bar
#    figure(1)
#        subplot(211)
#            hold on
#            set(gcf,'position',[50 50 1200 900])
#                plot(time1,bg_number,'lineW',1)
#                hold on
#                errorbar(time1,bg_number_mean,bg_number_std,'k','lineW',2)
#                if TimeLength==0
#                    ylabel('Number of meteor reflections','fontsize',fs,'fontweight','bold')
#                else
#                     ylabel(['Number of meteor reflections > ',num2str(TimeLength),' s'],'fontsize',fs,'fontweight','bold')
#                end
#                set(gca,'Xtick',0:3:24)
#                set(gca,'XtickLabel',{'00:00','','06:00','','12:00','','18:00','','00:00'},'fontSize',fs)
#                title(['Number of sporadic meteors, ',fln_station,' receiving station'],'fontSize',fs,'fontweight','bold')
#        %         legend([num2str(background_day(1)),'/',num2str(background_month)],[num2str(background_day(2)),'/',num2str(background_month)],[num2str(background_day(3)),'/',num2str(background_month)],'mean sporadic background')
#                grid on
#                %box
#        % numbers average and error bars + sine fit and weighted sine fit
#
#        subplot(212)
#        hold on
#        %set(gcf,'position',[50 50 1200 900])
#        errorbar(time1,bg_number_mean,bg_number_std,'k','lineW',2)
#        hold on
#        plot(time1,bg_number_mean_sinefit(1:24),'r','lineW',2)
#        plot(time1,bg_number_mean_weightedsinefit(1:24),'b','lineW',2)
#        if TimeLength==0
#            ylabel('Number of meteor reflections','fontsize',fs,'fontweight','bold')
#        else
#             ylabel(['Number of meteor reflections > ',num2str(TimeLength),' s'],'fontsize',fs,'fontweight','bold')
#        end
#        set(gca,'Xtick',0:3:24)
#        set(gca,'XtickLabel',{'00:00','','06:00','','12:00','','18:00','','00:00'},'fontSize',fs)
#        title(['background - ',fln_station],'fontSize',fs,'fontweight','bold')
#        legend('average background number','sine fit','weighted sine fit')
#        grid on
#        %box
#                %set(gcf,'paperpositionmode','auto')
#
#
# % data from indiv duration + average and error bars
#    figure(2)
#    subplot(211)
#        hold on
#        set(gcf,'position',[50 50 1200 900])
#            plot(time1,bg_duration,'lineW',1)
#            hold on
#            errorbar(time1,bg_duration_mean,bg_duration_std,'k','lineW',2)
#            if TimeLength==0
#                ylabel('Duration of meteor reflections','fontsize',fs,'fontweight','bold')
#            else
#                 ylabel(['Duration of meteor reflections > ',num2str(TimeLength),' s'],'fontsize',fs,'fontweight','bold')
#            end
#            set(gca,'Xtick',0:3:24)
#            set(gca,'XtickLabel',{'00:00','','06:00','','12:00','','18:00','','00:00'},'fontSize',fs)
#            title(['Duration of sporadic meteors, ',fln_station,' receiving station'],'fontSize',fs,'fontweight','bold')
#    %         legend([num2str(backgro_day(1)),'/',num2str(backgro_month)],[num2str(backgro_day(2)),'/',num2str(backgro_month)],[num2str(backgro_day(3)),'/',num2str(backgro_month)],'mean sporadic background')
#            grid on
#            %box
#    subplot(212)
#    hold on
#        %set(gcf,'position',[3000 50 1200 900])
#        errorbar(time1,bg_duration_mean,bg_duration_std,'k','lineW',2)
#        hold on
#        plot(time1,bg_duration_mean_sinefit(1:24),'r','lineW',2)
#        plot(time1,bg_duration_mean_weightedsinefit(1:24),'b','lineW',2)
#       if TimeLength==0
#            ylabel('Duration of meteor reflections','fontsize',fs,'fontweight','bold')
#        else
#             ylabel(['Duration of meteor reflections > ',num2str(TimeLength),' s'],'fontsize',fs,'fontweight','bold')
#        end
#        set(gca,'Xtick',0:3:24)
#        set(gca,'XtickLabel',{'00:00','','06:00','','12:00','','18:00','','00:00'},'fontSize',fs)
#        title(['background - ',fln_station],'fontSize',fs,'fontweight','bold')
#        legend('average background duration','sine fit','weighted sine fit')
#        grid on
#        %box
#
#
#% *******************
#%   SHOWER ACTIVITY
#% *******************
#
#date_label = cell(1,nb_shower_day*4+1);
#
#for i=1:nb_shower_day
#    j = 4*(i-1)+1;
#    date_label{j} = strcat(num2str(shower_day(i)),'/',num2str(shower_month,'%02d'));
#end
#date_label{nb_shower_day*4+1} = strcat(num2str(shower_day(i)+1),'/',num2str(shower_month,'%02d'));
#
#% limite des axes
#
#timeRange   = time2(end)-time2(1);
#sollonRange = SolarLongitude(end)-SolarLongitude(1);
#
#if Xaxis
#   Xvalues = SolarLongitude;
#   Xinf = SolarLongitude(1)-0.5*sollonRange/timeRange;
#   Xsup = SolarLongitude(end)+0.5*sollonRange/timeRange;
#   AxisFileName = '_SolLong'; % for name of the figure saved
#else
#   Xvalues = time2;
#   Xinf = time2(1)-0.5;
#   Xsup = time2(end)+0.5;
#   AxisFileName = '_UT';
#end
#YinfAc = 0;
#YsupNum = max(total_meteor_number)+5;
#YsupDur = max(total_meteor_duration)+10;
#YinfEle = min(elevation)-10;
#YsupEle = max(elevation)+10;
#
#figure(5)
#% total activity number + average values + sine fit + shower acti and
#% elevation as a function of UT or Solar longitude
#    hold on
#    set(gcf,'position',[2000 50 ,1200 900])
#    subplot(3,2,[1 4])
#        plot(Xvalues,total_meteor_number,'r','linew',2)
#        hold on
#        plot(Xvalues,bg_number_mean_rep,'ko')
#        plot(Xvalues,bg_number_mean_sinefit,'k','lineW',2)
#        plot(Xvalues,shower_number,'b','linew',2)
#        if TimeLength==0
#            ylabel('Number of meteor reflections','fontsize',fs,'fontweight','bold')
#        else
#            ylabel(['Number of meteor reflections > ',num2str(TimeLength),' s'],'fontsize',fs,'fontweight','bold')
#        end
#        if Xaxis
#            xlabel(' ','fontsize',fs,'fontweight','bold')
#            set(gca,'FontSize',fs)
#        else
#            set(gca,'Xtick',0:6:nb_shower_day*24)
#            set(gca,'XtickLabel',date_label,'FontSize',fs)
#        end
#        xlim([Xinf Xsup])
#        ylim([YinfAc YsupNum])
#        title([shower_name,' ',shower_year,', ',fln_station, ' receiving station'],'fontSize',fs,'fontweight','bold')
#        grid on
#    subplot(3,2,[5 6])
#        plot(Xvalues,elevation,'o','markersize',8,'markerfacecolor',[.76 .87 .78],'markeredgecolor',[0 .5 0])
#        if Xaxis
#            xlabel('Solar longitude','fontsize',fs,'fontweight','bold')
#            set(gca,'FontSize',fs)
#        else
#            set(gca,'Xtick',0:6:nb_shower_day*24)
#            set(gca,'XtickLabel',date_label,'FontSize',fs)
#        end
#        ylabel('Radiant elevation [<C2><B0>]','fontsize',fs,'fontweight','bold')
#        xlim([Xinf Xsup])
#        ylim([YinfEle YsupEle])
#        grid on
#
#
#figure(6)
#% total activity number + average values + weighted sine fit + shower acti and elevation as a function of UT or Solar longitude
#    hold on
#    set(gcf,'position',[2000 50 ,1200 900])
#    subplot(3,2,[1 4])
#        plot(Xvalues,total_meteor_number,'r','linew',2)
#        hold on
#        plot(Xvalues,bg_number_mean_rep,'ko')
#        plot(Xvalues,bg_number_mean_weightedsinefit,'k','lineW',2)
#        plot(Xvalues,shower_numberW,'b','linew',2)
#        if TimeLength==0
#            ylabel('Number of meteor reflections','fontsize',fs,'fontweight','bold')
#        else
#            ylabel(['Number of meteor reflections > ',num2str(TimeLength),' s'],'fontsize',fs,'fontweight','bold')
#        end
#        if Xaxis
#            xlabel(' ','fontsize',fs,'fontweight','bold')
#            set(gca,'FontSize',fs)
#        else
#            set(gca,'Xtick',0:6:nb_shower_day*24)
#            set(gca,'XtickLabel',date_label,'FontSize',fs)
#        end
#        xlim([Xinf Xsup])
#        ylim([YinfAc YsupNum])
#        title([shower_name,' ',shower_year,', ',fln_station, ' receiving station'],'fontSize',fs,'fontweight','bold')
#        grid on
#
#    subplot(3,2,[5 6])
#        plot(Xvalues,elevation,'o','markersize',8,'markerfacecolor',[.76 .87 .78],'markeredgecolor',[0 .5 0])
#        if Xaxis
#            xlabel('Solar Longitude','fontsize',fs,'fontweight','bold')
#            set(gca,'FontSize',fs)
#        else
#            set(gca,'Xtick',0:6:nb_shower_day*24)
#            set(gca,'XtickLabel',date_label,'FontSize',fs)
#        end
#        ylabel('Radiant elevation [<C2><B0>]','fontsize',fs,'fontweight','bold')
#        xlim([Xinf Xsup])
#        ylim([YinfEle YsupEle])
#        grid on
#
#
#
#figure(7)
#% total activity duration+ average values + sine fit + shower acti and elevation as a function of UT or Solar longitude
#    set(gcf,'position',[2000 50 ,1200 900])
#    subplot(3,2,[1 4])
#        plot(Xvalues,total_meteor_duration,'r','linew',2)
#        hold on
#        plot(Xvalues,bg_duration_mean_rep,'ko')
#        plot(Xvalues,bg_duration_mean_sinefit,'k','lineW',2)
#        plot(Xvalues,shower_duration,'b','linew',2)
#        if TimeLength==0
#            ylabel('Duration of meteor reflections','fontsize',fs,'fontweight','bold')
#        else
#            ylabel(['Duration of meteor > ',num2str(TimeLength),' s'],'fontsize',fs,'fontweight','bold')
#        end
#        if Xaxis
#            xlabel(' ','fontsize',fs,'fontweight','bold')
#            set(gca,'FontSize',fs)
#        else
#            set(gca,'Xtick',0:6:nb_shower_day*24)
#            set(gca,'XtickLabel',date_label,'FontSize',fs)
#        end
#        xlim([Xinf Xsup])
#        ylim([YinfAc YsupDur])
#        title([shower_name,' ',shower_year,', ',fln_station, ' receiving station'],'fontSize',fs,'fontweight','bold')
#        grid
#    subplot(3,2,[5 6])
#        plot(Xvalues,elevation,'o','markersize',8,'markerfacecolor',[.76 .87 .78],'markeredgecolor',[0 .5 0])
#        if Xaxis
#            xlabel('Solar Longitude','fontsize',fs,'fontweight','bold')
#            set(gca,'FontSize',fs)
#        else
#            set(gca,'Xtick',0:6:nb_shower_day*24)
#            set(gca,'XtickLabel',date_label,'FontSize',fs)
#        end
#        ylabel('Radiant elevation [<C2><B0>]','fontsize',fs,'fontweight','bold')
#        xlim([Xinf Xsup])
#        ylim([YinfEle YsupEle])
#        grid
#
#% total activity duration + average values + Weighted sine fit + shower acti and elevation
#figure(8)
#    set(gcf,'position',[2000 50 ,1200 900])
#    subplot(3,2,[1 4])
#        plot(Xvalues,total_meteor_duration,'r','linew',2)
#        hold on
#        plot(Xvalues,bg_duration_mean_rep,'ko')
#        plot(Xvalues,bg_duration_mean_weightedsinefit,'k','lineW',2)
#        plot(Xvalues,shower_durationW,'b','linew',2)
#
#        if Xaxis
#            xlabel(' ','fontsize',fs,'fontweight','bold')
#            set(gca,'FontSize',fs)
#        else
#            set(gca,'Xtick',0:6:nb_shower_day*24)
#            set(gca,'XtickLabel',date_label,'FontSize',fs)
#        end
#        if TimeLength==0
#            ylabel('Duration of meteor reflections','fontsize',fs,'fontweight','bold')
#        else
#            ylabel(['Duration of meteor > ',num2str(TimeLength),' s'],'fontsize',fs,'fontweight','bold')
#        end
#        xlim([Xinf Xsup])
#        ylim([YinfAc YsupDur])
#        title([shower_name,' ',shower_year,', ',fln_station, ' receiving station'],'fontSize',fs,'fontweight','bold')
#        grid on
#    subplot(3,2,[5 6])
#        plot(Xvalues,elevation,'o','markersize',8,'markerfacecolor',[.76 .87 .78],'markeredgecolor',[0 .5 0])
#        if Xaxis
#            xlabel('Solar Longitude','fontsize',fs,'fontweight','bold')
#            set(gca,'FontSize',fs)
#        else
#            set(gca,'Xtick',0:6:nb_shower_day*24)
#            set(gca,'XtickLabel',date_label,'FontSize',fs)
#        end
#        ylabel('Radiant elevation [<C2><B0>]','fontsize',fs,'fontweight','bold')
#        xlim([Xinf Xsup])
#        ylim([YinfEle YsupEle])
#        grid on
#
#% plot as a function of altitude and Solar Longitude
#        xlabels{1}='UT';xlabels{2}='Solar Longitude';
#        if TimeLength==0
#            ylabels{1} = 'Numbers of meteor reflections'; ylabels{2} = ' ';
#            ylabels2{1} = 'Duration of meteor reflections'; ylabels2{2}='';
#        else
#            ylabels{1} = ['Number of meteor reflections > ',num2str(TimeLength),' s'];ylabels{2}='';
#            ylabels2{1} = ['Duration of meteor > ',num2str(TimeLength),' s'];ylabels2{2}='';
#        end
#        ylabels3{1} = 'Radiant elevation [<C2><B0>]';ylabels3{2}=' ';
#        Xlim1 = [time2(1)-0.5 time2(end)+0.5];
#        Xlim2 = [SolarLongitude(1)-0.5*sollonRange/timeRange SolarLongitude(end)+0.5*sollonRange/timeRange];
#
#figure(9)
#        set(gcf,'position',[100 19 1290 952])
#    subplot(3,2,[1 4])
#        plotxx(time2,total_meteor_number,SolarLongitude,total_meteor_number,xlabels,ylabels,Xlim1,Xlim2,YinfAc,YsupNum,nb_shower_day,date_label)
#        hold on
#        plot(SolarLongitude,bg_number_mean_rep,'ko');
#        plot(SolarLongitude,bg_number_mean_sinefit,'k','lineW',2)
#        plot(SolarLongitude,shower_number,'b','linew',2)
#        title([shower_name,' ',shower_year,', ',fln_station, ' receiving station'],'fontSize',fs,'fontweight','bold')
#        grid on
#    subplot(3,2,[5 6])
#
#        plotxx2(time2,elevation,SolarLongitude,elevation,xlabels,ylabels3,Xlim1,Xlim2,YinfEle,YsupEle,nb_shower_day,date_label)
#
#
#figure(10)
#   set(gcf,'position',[100 19 1290 952])
#   subplot(3,2,[1 4])
#       plotxx(time2,total_meteor_number,SolarLongitude,total_meteor_number,xlabels,ylabels,Xlim1,Xlim2,YinfAc,YsupNum,nb_shower_day,date_label)
#       hold on
#       plot(SolarLongitude,bg_number_mean_rep,'ko');
#       plot(SolarLongitude,bg_number_mean_weightedsinefit,'k','lineW',2)
#       plot(SolarLongitude,shower_numberW,'b','linew',2)
#       title([shower_name,' ',shower_year,', ',fln_station, ' receiving station'],'fontSize',fs,'fontweight','bold')
#       grid on
#   subplot(3,2,[5 6])
#       plotxx2(time2,elevation,SolarLongitude,elevation,xlabels,ylabels3,Xlim1,Xlim2,YinfEle,YsupEle,nb_shower_day,date_label)
#
#figure(11)
#   set(gcf,'position',[100 19 1290 952])
#   subplot(3,2,[1 4])
#       plotxx(time2,total_meteor_duration,SolarLongitude,total_meteor_duration,xlabels,ylabels2,Xlim1,Xlim2,YinfAc,YsupDur,nb_shower_day,date_label)
#       hold on
#       plot(SolarLongitude,bg_duration_mean_rep,'ko');
#       plot(SolarLongitude,bg_duration_mean_sinefit,'k','lineW',2)
#       plot(SolarLongitude,shower_duration,'b','linew',2)
#       title([shower_name,' ',shower_year,', ',fln_station, ' receiving station'],'fontSize',fs,'fontweight','bold')
#       grid on
#   subplot(3,2,[5 6])
#       plotxx2(time2,elevation,SolarLongitude,elevation,xlabels,ylabels3,Xlim1,Xlim2,YinfEle,YsupEle,nb_shower_day,date_label)
#
#figure(12)
#    YsupNum=max(total_meteor_duration)+10;
#    set(gcf,'position',[100 19 1290 952])
#    subplot(3,2,[1 4])
#        plotxx(time2,total_meteor_duration,SolarLongitude,total_meteor_duration,xlabels,ylabels2,Xlim1,Xlim2,YinfAc,YsupDur,nb_shower_day,date_label)
#        hold on
#        plot(SolarLongitude,bg_duration_mean_rep,'ko');
#        plot(SolarLongitude,bg_duration_mean_weightedsinefit,'k','lineW',2)
#        plot(SolarLongitude,shower_durationW,'b','linew',2)
#        title([shower_name,' ',shower_year,', ',fln_station, ' receiving station'],'fontSize',fs,'fontweight','bold')
#        grid on
#    subplot(3,2,[5 6])
#        plotxx2(time2,elevation,SolarLongitude,elevation,xlabels,ylabels3,Xlim1,Xlim2,YinfEle,YsupEle,nb_shower_day,date_label)
#
#
#
#% save plot
#if saveFig
#
#    if TimeLength == 0
#        saveas(figure(1),[shower_name,'_',shower_year,'_background_number_',fln_station],'png')
#        saveas(figure(2),[shower_name,'_',shower_year,'_background_duration_',fln_station],'png')
#        saveas(figure(5),[shower_name,'_',shower_year,'_activity_number_SineFit',fln_station,AxisFileName],'png')
#        saveas(figure(6),[shower_name,'_',shower_year,'_activity_number_WeightSineFit',fln_station,AxisFileName],'png')
#        saveas(figure(7),[shower_name,'_',shower_year,'_activity_duration_SineFit',fln_station,AxisFileName],'png')
#        saveas(figure(8),[shower_name,'_',shower_year,'_activity_duration_WeightSineFit',fln_station,AxisFileName],'png')
#        saveas(figure(9),[shower_name,'_',shower_year,'_activity_number_SineFit',fln_station,'_UT_SolLong'],'png')
#        saveas(figure(10),[shower_name,'_',shower_year,'_activity_number_WeightSineFit',fln_station,'_UT_SolLong'],'png')
#        saveas(figure(11),[shower_name,'_',shower_year,'_activity_duration_SineFit',fln_station,'_UT_SolLong'],'png')
#        saveas(figure(12),[shower_name,'_',shower_year,'_activity_duration_WeightSineFit',fln_station,'_UT_SolLong'],'png')
#    else
#       saveas(figure(1),[shower_name,'_',shower_year,'_background_number_',fln_station,'_',num2str(TimeLength,'%02d'),'sec'],'png')
#       saveas(figure(2),[shower_name,'_',shower_year,'_background_duration_',fln_station,'_',num2str(TimeLength,'%02d'),'sec'],'png')
#       saveas(figure(5),[shower_name,'_',shower_year,'_activity_number_SineFit',fln_station,'_',num2str(TimeLength,'%02d'),'sec',AxisFileName],'png')
#       saveas(figure(6),[shower_name,'_',shower_year,'_activity_number_WeightSineFit',fln_station,'_',num2str(TimeLength,'%02d'),'sec',AxisFileName],'png')
#       saveas(figure(7),[shower_name,'_',shower_year,'_activity_duration_SineFit',fln_station,'_',num2str(TimeLength,'%02d'),'sec',AxisFileName],'png')
#       saveas(figure(8),[shower_name,'_',shower_year,'_activity_duration_WeightSineFit',fln_station,'_',num2str(TimeLength,'%02d'),'sec',AxisFileName],'png')
#       saveas(figure(9),[shower_name,'_',shower_year,'_activity_number_SineFit',fln_station,'_',num2str(TimeLength,'%02d'),'sec','_UT_SolLong'],'png')
#       saveas(figure(10),[shower_name,'_',shower_year,'_activity_number_WeightSineFit',fln_station,'_',num2str(TimeLength,'%02d'),'sec','_UT_SolLong'],'png')
#       saveas(figure(11),[shower_name,'_',shower_year,'_activity_duration_SineFit',fln_station,'_',num2str(TimeLength,'%02d'),'sec','_UT_SolLong'],'png')
#       saveas(figure(12),[shower_name,'_',shower_year,'_activity_duration_WeightSineFit',fln_station,'_',num2str(TimeLength,'%02d'),'sec','_UT_SolLong'],'png')
#    end
#
#        % create directory to store png and fig plots
#        StorageDir = strcat('mkdir -p ./',shower_name,shower_year,'/',fln_station,'/','png');%'{fig,png}');
#        MVcreateDirCommand = sprintf(StorageDir);
#        system(MVcreateDirCommand);
#
#
#    MVPNGcommand = sprintf(strcat('mv *.png ./',shower_name,shower_year,'/',fln_station,'/png/'));
#    %MVFIGcommand = sprintf(strcat('mv *.fig ./',shower_name,shower_year,'/',fln_station,'/fig/'));
#    system(MVPNGcommand);
#    %system(MVFIGcommand);
#end
#
#fid15 = fopen(strcat(shower_name,shower_year,'_',fln_station,'_results_',...
#    num2str(TimeLength),'.txt'),'w');
#for i=1:size(time2,2)
#    fprintf(fid15,'%d %f %f \n',time2(i),shower_number(i),shower_duration(i));
#end
#fclose(fid15);
#
#fid16 = fopen(strcat(shower_name,shower_year,'_',fln_station,'_results_',...
#    num2str(TimeLength),'_background.txt'),'w');
#for i=1:size(time2,2)
#    fprintf(fid16,'%d %f %f %f %f \n',time2(i),bg_number_mean_weightedsinefit(i), ...
#       bg_number_mean_sinefit(i), bg_duration_mean_weightedsinefit(i), ...
#       bg_duration_mean_sinefit(i));
#end
#fclose(fid16);
#
#fid17 = fopen(strcat(shower_name,shower_year,'_',fln_station,'_results_',...
#    num2str(TimeLength),'_background_individualdays.txt'),'w');
#for i=1:24
#    fprintf(fid17,'%d %f %f %f %f \n',time2(i),bg_number_mean(i), ...
#       bg_number_std(i), bg_duration_mean(i), bg_duration_std(i)) ;
#end
#fclose(fid17);
#
#MVTXTcommand = ['mv',' ',shower_name,shower_year,'*.txt ./Comparison/',shower_name];
#system(MVTXTcommand);        