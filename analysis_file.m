clear all
close all
clc

opts = detectImportOptions('merge_nathan_ambiguous.csv', 'Delimiter', ';'); %%change name of merged file
opts = setvartype(opts, 'key_pressed', 'char');
T    = readtable('merge_nathan_ambiguous.csv', opts); %%change name here as well

T.timestamp_ms = T.timestamp_pc / 1000;   % µs ? ms
t   = T.timestamp_ms;
eta = fillmissing(T.etat, 'constant', 0);


label = repmat(' ', height(T), 1);
label(strcmp(T.key_pressed, 'VERTICAL'))   = 'V';
label(strcmp(T.key_pressed, 'HORIZONTAL')) = 'H';

kp_idx = find(label == 'V' | label == 'H');

seg_starts = kp_idx(1);
seg_labels = label(kp_idx(1));

for i = 2:numel(kp_idx)
    if label(kp_idx(i)) ~= label(kp_idx(i-1))
        seg_starts(end+1) = kp_idx(i);   %#ok<SAGROW>  ignores warnings
        seg_labels(end+1) = label(kp_idx(i)); %#ok<SAGROW>
    end
end

seg_ends = [seg_starts(2:end) - 1, kp_idx(end)];


col_V  = [0.85 0.18 0.18];   % red  VERTICAL
col_H  = [0.10 0.55 0.85];   % blue   HORIZONTAL
col_bg = [0.98 0.98 0.98];
x_lim  = [t(1), t(end)];

fig = figure('Name', 'Timeline VERTICAL / HORIZONTAL & State','NumberTitle', 'off', 'Color', col_bg, 'Position', [60 100 1500 700]);

ax1 = subplot(2, 1, 1, 'Parent', fig, 'Color', [1 1 1]);
hold(ax1, 'on');


patch(ax1, [x_lim(1) x_lim(2) x_lim(2) x_lim(1)],[0.8 0.8 1.2 1.2],[0.88 0.88 0.88], 'EdgeColor', 'none', 'HandleVisibility', 'off');


for k = 1:numel(seg_starts)
    t0 = t(seg_starts(k));
    t1 = t(seg_ends(k));
    if seg_labels(k) == 'V'
        col = col_V;
    else
        col = col_H;
    end
    patch(ax1, [t0 t1 t1 t0], [0.8 0.8 1.2 1.2], col, 'EdgeColor', 'none', 'HandleVisibility', 'off');
end


patch(ax1, NaN, NaN, col_V, 'EdgeColor', 'none', 'DisplayName', 'VERTICAL');
patch(ax1, NaN, NaN, col_H, 'EdgeColor', 'none', 'DisplayName', 'HORIZONTAL');

hold(ax1, 'off');

set(ax1, 'YTick', [], 'XTickLabel', [], 'FontSize', 10, 'Box', 'on');
xlim(ax1, x_lim);
ylim(ax1, [0.6 1.4]);
title(ax1, 'VERTICAL (red) / HORIZONTAL (blue)', ...
      'FontSize', 12, 'FontWeight', 'bold');
legend(ax1, 'Location', 'best', 'FontSize', 11);


ax2 = subplot(2, 1, 2, 'Parent', fig, 'Color', [1 1 1]);

stairs(ax2, t, eta, 'Color', [0.2 0.2 0.2], 'LineWidth', 1.4, 'DisplayName', 'State');

xlabel(ax2, 'Time (ms)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel(ax2, 'State', 'FontSize', 11, 'FontWeight', 'bold');
title(ax2, 'State (0/1)', 'FontSize', 12, 'FontWeight', 'bold', 'Color', [0.4 0.4 0.4]);
set(ax2, 'YTick', [0 1], 'YTickLabel', {'0','1'},'FontSize', 10, 'Box', 'on');
xlim(ax2, x_lim);
ylim(ax2, [-0.15 1.25]);
grid(ax2, 'on');
set(ax2, 'GridAlpha', 0.2);
legend(ax2, 'Location', 'best', 'FontSize', 11);

linkaxes([ax1, ax2], 'x');
