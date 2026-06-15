using System;
using System.IO;
using System.Text;
using System.ComponentModel;
using ATAS.Indicators;
using Utils.Common.Logging;

namespace ATAS.Indicators.Technical
{
    [DisplayName("Claude Data Export")]
    [Description("Exports OHLCV + cluster data to local JSON file on each bar close for Claude Code consumption")]
    public class ClaudeDataExport : Indicator
    {
        private int _lastExportedBar = -1;
        private string _outputDir;
        private string _barsFile;
        private string _briefFile;
        private readonly StringBuilder _recentBars = new StringBuilder();

        [DisplayName("Output Directory")]
        [Description("Directory to write JSON files")]
        public string OutputDirectory { get; set; } = @"G:\PriceAction\交易日志\atas";

        [DisplayName("EMA Period")]
        [Description("EMA period for trend detection")]
        public int EmaPeriod
        {
            get => _emaPeriod;
            set
            {
                _emaPeriod = value;
                RecalculateValues();
            }
        }
        private int _emaPeriod = 20;

        [DisplayName("Recent Bars Count")]
        [Description("Number of recent bars to keep in rolling JSON")]
        public int RecentBarsCount
        {
            get => _recentBarsCount;
            set
            {
                _recentBarsCount = value;
                RecalculateValues();
            }
        }
        private int _recentBarsCount = 20;

        private decimal _emaValue = 0;
        private decimal _emaMultiplier = 0;
        private bool _emaInitialized = false;

        public ClaudeDataExport() : base(true)
        {
        }

        protected override void OnInitialize()
        {
            _outputDir = OutputDirectory;
            if (!Directory.Exists(_outputDir))
                Directory.CreateDirectory(_outputDir);

            _barsFile = Path.Combine(_outputDir, "recent-20-bars.json");
            _briefFile = Path.Combine(_outputDir, "latest-atas-brief.md");

            _emaMultiplier = 2m / (_emaPeriod + 1);
            _lastExportedBar = -1;
            _emaInitialized = false;

            this.LogInfo("ClaudeDataExport initialized. Output: " + _outputDir);
        }

        protected override void OnCalculate(int bar, decimal value)
        {
            var candle = GetCandle(bar);

            if (bar < _emaPeriod)
            {
                if (bar == _emaPeriod - 1)
                {
                    decimal sum = 0;
                    for (int i = 0; i <= bar; i++)
                        sum += GetCandle(i).Close;
                    _emaValue = sum / _emaPeriod;
                    _emaInitialized = true;
                }
            }
            else if (_emaInitialized)
            {
                _emaValue = (candle.Close - _emaValue) * _emaMultiplier + _emaValue;
            }

            this[bar] = _emaValue;

            // 只在最新 bar 处理导出逻辑
            if (bar != CurrentBar - 1)
                return;

            // 导出上一根已完成的 bar（bar - 1），不是当前正在形成的 bar
            // 当新 bar 的第一个 tick 到达时，bar-1 才刚完整收盘
            int completedBar = bar - 1;
            if (completedBar < _emaPeriod || completedBar == _lastExportedBar)
                return;

            _lastExportedBar = completedBar;

            try
            {
                var completedCandle = GetCandle(completedBar);
                ExportRecentBars(completedBar);
                ExportBrief(completedBar, completedCandle);
            }
            catch (Exception ex)
            {
                this.LogError("ClaudeDataExport write error: " + ex.Message);
            }
        }

        private void ExportRecentBars(int currentBar)
        {
            var sb = new StringBuilder();
            sb.AppendLine("[");

            int startBar = Math.Max(0, currentBar - _recentBarsCount + 1);
            for (int i = startBar; i <= currentBar; i++)
            {
                var c = GetCandle(i);
                decimal delta = c.Delta;
                decimal range = c.High - c.Low;
                decimal bodyPct = range > 0 ? Math.Round(Math.Abs(c.Close - c.Open) / range * 100, 1) : 0;
                decimal deltaPct = c.Volume > 0 ? Math.Round(delta / c.Volume * 100, 1) : 0;

                sb.Append("  {");
                sb.Append($"\"bar_index\":{i}");
                sb.Append($",\"open\":{c.Open}");
                sb.Append($",\"high\":{c.High}");
                sb.Append($",\"low\":{c.Low}");
                sb.Append($",\"close\":{c.Close}");
                sb.Append($",\"volume\":{c.Volume}");
                sb.Append($",\"delta\":{delta}");
                sb.Append($",\"delta_pct\":{deltaPct}");
                sb.Append($",\"max_delta\":{c.MaxDelta}");
                sb.Append($",\"min_delta\":{c.MinDelta}");
                sb.Append($",\"range\":{range}");
                sb.Append($",\"body_pct\":{bodyPct}");
                sb.Append($",\"ema{_emaPeriod}\":{Math.Round(this[i], 2)}");
                sb.Append($",\"time\":\"{c.Time:yyyy-MM-ddTHH:mm:ssZ}\"");
                sb.Append("}");

                if (i < currentBar)
                    sb.AppendLine(",");
                else
                    sb.AppendLine();
            }

            sb.AppendLine("]");

            File.WriteAllText(_barsFile, sb.ToString(), Encoding.UTF8);
        }

        private void ExportBrief(int bar, IndicatorCandle candle)
        {
            var barOpen = candle.Time.AddHours(8);
            var barClose = barOpen.AddMinutes(5);

            decimal bodySize = Math.Abs(candle.Close - candle.Open);
            decimal totalSize = candle.High - candle.Low;
            decimal bodyRatio = totalSize > 0 ? bodySize / totalSize * 100 : 0;
            decimal deltaPct = candle.Volume > 0 ? candle.Delta * 100m / candle.Volume : 0;
            string direction = candle.Close > candle.Open ? "bullish" : "bearish";
            string barType;
            if (bodyRatio > 70) barType = "trend bar";
            else if (bodyRatio < 30) barType = "doji";
            else barType = "mixed";

            string deltaRead;
            if (deltaPct > 15) deltaRead = "delta 偏多";
            else if (deltaPct < -15) deltaRead = "delta 偏空";
            else deltaRead = "delta 中性";

            decimal emaDist = candle.Close - _emaValue;
            string emaRelation = emaDist >= 0 ? "above" : "below";
            string bias;
            if (emaDist > 3) bias = "long";
            else if (emaDist < -3) bias = "short";
            else bias = "neutral";

            var sb = new StringBuilder();
            sb.AppendLine("# Codex ATAS 数据推送");
            sb.AppendLine();
            sb.AppendLine("## 最新 5m K");
            sb.AppendLine($"- 时间：{barOpen:HH:mm}-{barClose:HH:mm} 北京时间");
            sb.AppendLine($"- 标的：GCQ6");
            sb.AppendLine($"- OHLCV：O {candle.Open} / H {candle.High} / L {candle.Low} / C {candle.Close} / V {candle.Volume}");
            sb.AppendLine($"- EMA{_emaPeriod}：{Math.Round(_emaValue, 2)}");
            sb.AppendLine($"- bar_index：{bar}");
            sb.AppendLine();
            sb.AppendLine("## 本地预分析");
            sb.AppendLine($"- Bias：{bias}");
            sb.AppendLine($"- 方向：{direction}");
            sb.AppendLine($"- 收盘距 EMA{_emaPeriod}：{(emaDist >= 0 ? "+" : "")}{Math.Round(emaDist, 1)} 点（{emaRelation}）");
            sb.AppendLine();
            sb.AppendLine("## Order Flow 数据");
            sb.AppendLine($"- Delta：{candle.Delta}（占比 {(deltaPct >= 0 ? "+" : "")}{Math.Round(deltaPct, 1)}%）");
            sb.AppendLine($"- MaxDelta：{candle.MaxDelta} / MinDelta：{candle.MinDelta}");
            sb.AppendLine($"- 振幅：{Math.Round(totalSize, 1)} 点");
            sb.AppendLine($"- 实体占比：{Math.Round(bodyRatio, 1)}%");
            sb.AppendLine($"- 判读：{deltaRead} + {barType}");

            File.WriteAllText(_briefFile, sb.ToString(), Encoding.UTF8);
        }
    }
}
