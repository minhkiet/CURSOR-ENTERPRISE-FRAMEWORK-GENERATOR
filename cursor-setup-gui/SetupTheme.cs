using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

namespace CursorSetup
{
    /// <summary>
    /// Centralized visual theme — Modern Indigo + Slate palette.
    /// Used by SetupForm and dynamic tab builders. Keep helpers small,
    /// avoid abstractions for single-use cases.
    /// </summary>
    internal static class SetupTheme
    {
        // === Palette (Tailwind indigo + slate, mirrored to System.Drawing) ===
        public static readonly Color Indigo600 = Color.FromArgb(79, 70, 229);   // primary accent
        public static readonly Color Indigo500 = Color.FromArgb(99, 102, 241);  // hover
        public static readonly Color Indigo400 = Color.FromArgb(129, 140, 248); // soft accent
        public static readonly Color Indigo50  = Color.FromArgb(238, 242, 255); // tint

        public static readonly Color Slate900 = Color.FromArgb(15, 23, 42);    // headings
        public static readonly Color Slate700 = Color.FromArgb(51, 65, 85);    // body
        public static readonly Color Slate500 = Color.FromArgb(100, 116, 139); // muted
        public static readonly Color Slate400 = Color.FromArgb(148, 163, 184); // divider
        public static readonly Color Slate200 = Color.FromArgb(226, 232, 240); // border
        public static readonly Color Slate100 = Color.FromArgb(241, 245, 249); // panel
        public static readonly Color Slate50  = Color.FromArgb(248, 250, 252); // surface

        public static readonly Color Emerald600 = Color.FromArgb(5, 150, 105); // install CTA
        public static readonly Color Emerald500 = Color.FromArgb(16, 185, 129);// install hover
        public static readonly Color Rose600   = Color.FromArgb(225, 29, 72); // cancel/close

        // === Surfaces ===
        public static readonly Color FormBack       = Slate50;
        public static readonly Color HeaderBack     = Color.White;
        public static readonly Color TabBack        = Color.White;
        public static readonly Color TabSelectedBg  = Color.White;
        public static readonly Color TabUnselectedBg = Color.FromArgb(248, 250, 252);
        public static readonly Color CardBack       = Color.White;
        public static readonly Color LogBack        = Color.FromArgb(15, 23, 42);  // dark slate-900
        public static readonly Color LogFore        = Color.FromArgb(226, 232, 240);
        public static readonly Color ProgressTrack  = Color.FromArgb(226, 232, 240);
        public static readonly Color StatusIdle     = Slate500;
        public static readonly Color StatusActive   = Indigo600;
        public static readonly Color StatusDone     = Emerald600;

        // === Typography ===
        public static readonly Font FontTitle    = new Font("Segoe UI Semibold", 16.5F, FontStyle.Bold);
        public static readonly Font FontSubtitle = new Font("Segoe UI", 9.5F);
        public static readonly Font FontTab      = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);
        public static readonly Font FontLabel    = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);
        public static readonly Font FontBody     = new Font("Segoe UI", 9.5F);
        public static readonly Font FontMono     = new Font("Cascadia Mono, Consolas, Segoe UI", 9.5F);
        public static readonly Font FontCta      = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);

        // === Button paint — flat modern with hover/press states ============
        /// <summary>
        /// Paint a flat rounded-rect button with hover/pressed feedback.
        /// Use inside a Button's Paint event with FlatStyle.Flat.
        /// </summary>
        public static void PaintButton(Button btn, PaintEventArgs e, Color baseColor, Color hoverColor)
        {
            var g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

            var rect = btn.ClientRectangle;
            rect.Inflate(-1, -1);
            using (var path = RoundedRect(rect, 6))
            {
                Color fill = btn.FlatAppearance.MouseDownBackColor != Color.Empty && Control.MouseButtons == MouseButtons.Left
                    ? Darken(baseColor, 0.10f)
                    : (btn.ClientRectangle.Contains(btn.PointToClient(Cursor.Position)) ? hoverColor : baseColor);

                using (var b = new SolidBrush(fill))
                    g.FillPath(b, path);

                TextRenderer.DrawText(
                    g, btn.Text, btn.Font, rect,
                    btn.ForeColor,
                    TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis);
            }
        }

        /// <summary>
        /// Paint the primary install CTA. Gradient indigo→emerald feels "go".
        /// </summary>
        public static void PaintPrimaryCta(Button btn, PaintEventArgs e)
        {
            var g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

            var rect = btn.ClientRectangle;
            rect.Inflate(-1, -1);
            using (var path = RoundedRect(rect, 8))
            using (var lg = new LinearGradientBrush(rect, Indigo600, Emerald600, LinearGradientMode.Horizontal))
            {
                bool hovered = btn.ClientRectangle.Contains(btn.PointToClient(Cursor.Position));
                if (hovered)
                {
                    using (var lg2 = new LinearGradientBrush(rect, Indigo500, Emerald500, LinearGradientMode.Horizontal))
                        g.FillPath(lg2, path);
                }
                else
                {
                    g.FillPath(lg, path);
                }

                TextRenderer.DrawText(
                    g, btn.Text, btn.Font, rect,
                    Color.White,
                    TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis);
            }
        }

        /// <summary>
        /// Paint a subtle ghost button (cancel).
        /// </summary>
        public static void PaintGhostButton(Button btn, PaintEventArgs e)
        {
            var g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

            var rect = btn.ClientRectangle;
            rect.Inflate(-1, -1);
            using (var path = RoundedRect(rect, 6))
            {
                bool hovered = btn.ClientRectangle.Contains(btn.PointToClient(Cursor.Position));
                Color fill = hovered ? Slate100 : Color.White;
                Color border = hovered ? Slate400 : Slate200;

                using (var b = new SolidBrush(fill))
                    g.FillPath(b, path);
                using (var p = new Pen(border, 1))
                    g.DrawPath(p, path);

                TextRenderer.DrawText(
                    g, btn.Text, btn.Font, rect,
                    Slate700,
                    TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis);
            }
        }

        // === Tab paint — Linear/Notion-style underline indicator ===========
        public static void PaintTab(DrawItemEventArgs e, TabControl tabs, string text, bool selected)
        {
            var g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

            var rect = e.Bounds;
            // Background — subtle tint when selected, transparent when not
            using (var bg = new SolidBrush(selected ? Indigo50 : Color.White))
                g.FillRectangle(bg, rect);

            // Text color
            Color textColor = selected ? Indigo600 : Slate500;
            using (var f = (Font)SetupTheme.FontTab.Clone())
            {
                var font = selected ? new Font(f, FontStyle.Bold) : f;
                var textRect = new Rectangle(rect.X, rect.Y, rect.Width, rect.Height - 3);
                TextRenderer.DrawText(g, text, font, textRect, textColor,
                    TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis);
            }

            // Bottom indicator — 3px line, indigo when selected, transparent otherwise
            if (selected)
            {
                int indicatorH = 3;
                var indRect = new Rectangle(rect.X + 8, rect.Bottom - indicatorH, rect.Width - 16, indicatorH);
                using (var b = new SolidBrush(Indigo600))
                    g.FillRectangle(b, indRect);
            }
        }

        // === Progress bar paint — rounded track + filled portion ==========
        public static void PaintProgress(ProgressBar pb, PaintEventArgs e)
        {
            var g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;

            int h = pb.Height;
            int radius = Math.Min(6, h / 2);
            var fullRect = new Rectangle(0, 0, pb.Width - 1, h - 1);

            using (var trackPath = RoundedRect(fullRect, radius))
            using (var trackBrush = new SolidBrush(ProgressTrack))
            {
                g.FillPath(trackBrush, trackPath);
            }

            if (pb.Value > 0)
            {
                int filledWidth = (int)(pb.Width * ((double)pb.Value / pb.Maximum));
                if (filledWidth < radius * 2) filledWidth = radius * 2;
                var fillRect = new Rectangle(0, 0, filledWidth, h - 1);

                using (var fillPath = RoundedRect(fillRect, radius))
                using (var lg = new LinearGradientBrush(fillRect, Indigo600, Emerald600, LinearGradientMode.Horizontal))
                {
                    g.FillPath(lg, fillPath);
                }
            }
        }

        // === Card paint — subtle border, white fill ========================
        public static void PaintCard(Control c, PaintEventArgs e)
        {
            var g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;

            using (var path = RoundedRect(c.ClientRectangle, 10))
            using (var bg = new SolidBrush(CardBack))
            using (var pen = new Pen(Slate200, 1))
            {
                g.FillPath(bg, path);
                g.DrawPath(pen, path);
            }
        }

        // === Helpers =======================================================
        public static GraphicsPath RoundedRect(Rectangle bounds, int radius)
        {
            int d = radius * 2;
            var path = new GraphicsPath();
            if (bounds.Width < d || bounds.Height < d)
            {
                path.AddRectangle(bounds);
                return path;
            }
            path.AddArc(bounds.X, bounds.Y, d, d, 180, 90);
            path.AddArc(bounds.Right - d, bounds.Y, d, d, 270, 90);
            path.AddArc(bounds.Right - d, bounds.Bottom - d, d, d, 0, 90);
            path.AddArc(bounds.X, bounds.Bottom - d, d, d, 90, 90);
            path.CloseFigure();
            return path;
        }

        public static Color Darken(Color c, float factor)
        {
            return Color.FromArgb(
                (int)(c.R * (1 - factor)),
                (int)(c.G * (1 - factor)),
                (int)(c.B * (1 - factor)));
        }

        /// <summary>
        /// Wire a button to be themed via SetupTheme. Single helper, no class
        /// explosion — capture the colors and handler by closure.
        /// </summary>
        public static void WireFlatButton(Button btn, Color baseColor, Color hoverColor, Action<Button, PaintEventArgs> paint)
        {
            btn.FlatStyle = FlatStyle.Flat;
            btn.FlatAppearance.BorderSize = 0;
            btn.Cursor = Cursors.Hand;
            btn.Paint += (s, e) => paint?.Invoke((Button)s, e);
            btn.MouseEnter += (s, e) => ((Button)s).Invalidate();
            btn.MouseLeave += (s, e) => ((Button)s).Invalidate();
        }
    }
}
