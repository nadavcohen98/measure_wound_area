% File paths
file_NIH3T3 = '/Users/nadavcohen/Desktop/Universuty/final_project/matlab/wound_size_table_NIH3T3.xlsx';
file_C2C12 = '/Users/nadavcohen/Desktop/Universuty/final_project/matlab/wound_size_table_C2C12.xlsx';

% Load both tables
data1 = readtable(file_NIH3T3);
data2 = readtable(file_C2C12);

% Extract time and group info
plate_ids1 = data1.Var1;
plate_ids2 = data2.Var1;
group_ids1 = floor(plate_ids1);
group_ids2 = floor(plate_ids2);

pixel_values1 = data1{:, 2:end};
pixel_values2 = data2{:, 2:end};

time_points = 0:(size(pixel_values1, 2)-1);
t_fine = linspace(min(time_points), max(time_points), 1000);

% Shared parameters
group_names = {'Control', '5 min laser', '8 min laser', '10 min laser'};
colors = lines(2); % One for each cell type

% Exponential model
model = fittype(@(k, t) exp(-k * t), ...
                'independent', 't', 'coefficients', {'k'});

for g = 1:4
    % Prepare figure per group
    figure; hold on;
    title(['Comparison for Group: ' group_names{g}]);
    xlabel('Time (hours)');
    ylabel('Normalized Wound Size');
    grid on;

    for d = 1:2  % d=1 for NIH3T3, d=2 for C2C12
        if d == 1
            group_data = pixel_values1(group_ids1 == g, :);
            label = 'NIH3T3';
        else
            group_data = pixel_values2(group_ids2 == g, :);
            label = 'C2C12';
        end

        % Normalize by t=0
        normalized = group_data ./ group_data(:, 1);
        mean_vals = mean(normalized, 1);

        % Fit exponential decay to mean
        fitresult = fit(time_points', mean_vals', model, 'StartPoint', 0.2);
        k = fitresult.k;
        y_fit = exp(-k * t_fine);

        % Individual curve fits
        n_wounds = size(normalized, 1);
        y_individual = zeros(n_wounds, length(time_points));
        for i = 1:n_wounds
            wound = normalized(i, :);
            try
                fit_i = fit(time_points', wound', model, 'StartPoint', 0.2);
                y_i = exp(-fit_i.k * time_points);
                y_individual(i, :) = y_i;
            catch
                y_individual(i, :) = NaN;
            end
        end

        y_std = std(y_individual, 0, 1, 'omitnan');

        % Plot mean fit
        plot(t_fine, y_fit, '-', 'LineWidth', 2, ...
            'Color', colors(d, :), 'DisplayName', [label ' Fit']);

        % Plot error bars
        h = errorbar(time_points, exp(-k * time_points), y_std, ...
            'Color', colors(d,:), 'LineStyle', 'none', ...
            'CapSize', 5, 'LineWidth', 1.2, ...
            'DisplayName', ['STD ' label]);
        h.Annotation.LegendInformation.IconDisplayStyle = 'on';
    end

    legend('Location', 'best');
end