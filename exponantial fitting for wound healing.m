% Load data
filename = '/Users/nadavcohen/Desktop/Universuty/final_project/matlab/wound_size_table_C2C12.xlsx';
data = readtable(filename);
plate_ids = data.Var1;
pixel_values = data{:, 2:end};
time_points = 0:(size(pixel_values, 2)-1);

% Normalize each plate by its t=0 value
normalized_values = pixel_values ./ pixel_values(:, 1);

% Prepare plot
figure; hold on;
title('Normalized Wound Size for Each Plate');
xlabel('Time (hours)');
ylabel('Normalized Wound Size');

% Generate a large distinct colormap (e.g., parula or turbo or hsv)
num_plates = length(plate_ids);
cmap = parula(num_plates);  % You can also use 'jet', 'lines', 'hsv', etc.

% Plot each plate’s normalized curve with a unique color
for i = 1:num_plates
    plot(time_points, normalized_values(i, :), '-', ...
         'LineWidth', 1.5, ...
         'Color', cmap(i, :), ...
         'DisplayName', sprintf('Plate %.1f', plate_ids(i)));
end

% Make the legend scrollable if too many items
legend('show', 'Location', 'eastoutside');
grid on;