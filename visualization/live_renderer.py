"""
EvolveAI — Live Renderer (Pygame)
===================================

Grid dünyayı gerçek zamanlı render eder. Demo gününün ana görsel kısmı.

ÖZELLİKLER:
    - Renk kodlu ajanlar (strateji tipine göre)
    - Can/enerji barları
    - Saldırı efektleri (kısa flash)
    - Kaynak ve engel görselleştirme
    - HUD: nesil, adım, hayatta kalan ajan sayısı
    - FPS sayacı

KULLANIM:
    renderer = LiveRenderer()
    renderer.render(env)
    renderer.close()
"""

from __future__ import annotations

from typing import Optional

try:
    import pygame
except ImportError:
    pygame = None

from config import CONFIG


class LiveRenderer:
    """Pygame tabanlı canlı render.

    LAZY INIT: Pygame ancak ilk render çağrısında yüklenir, bu sayede
    headless training'de overhead yok.
    """

    def __init__(self, headless: bool = False):
        if pygame is None:
            raise ImportError("Pygame yüklü değil: pip install pygame==2.5.2")

        self.config = CONFIG.viz
        self.world_config = CONFIG.world
        self.headless = headless
        self.screen: Optional["pygame.Surface"] = None
        self.clock = None
        self.font = None
        self._initialized = False

    def _lazy_init(self) -> None:
        """İlk çağrıda pygame'i başlat.

        TODO[Sonnet]: Implement
            pygame.init()
            width = GRID_SIZE[1] * CELL_SIZE_PX + 300  # +300 HUD için
            height = GRID_SIZE[0] * CELL_SIZE_PX
            if self.headless:
                self.screen = pygame.Surface((width, height))
            else:
                self.screen = pygame.display.set_mode((width, height))
                pygame.display.set_caption("EvolveAI - Live Simulation")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("Arial", 16)
            self._initialized = True
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 7'de doldurulacak")

    def render(self, env, info: Optional[dict] = None) -> Optional["np.ndarray"]:
        """Tek frame çiz.

        TODO[Sonnet]: Implement
            if not self._initialized: self._lazy_init()
            self.screen.fill(BACKGROUND_COLOR)
            self._draw_grid()
            self._draw_obstacles(env.obstacles)
            self._draw_resources(env.resources)
            self._draw_agents(env.agents)
            self._draw_hud(env, info)
            if not self.headless:
                pygame.event.pump()  # Windows pencere donmasını önle
                pygame.display.flip()
                self.clock.tick(FPS)
            return pygame.surfarray.array3d(self.screen)  # RGB array (replay için)
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 7'de doldurulacak")

    def _draw_grid(self) -> None:
        """Grid çizgilerini çiz.

        TODO[Sonnet]: Implement nested for loop, pygame.draw.line
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 7'de doldurulacak")

    def _draw_agents(self, agents) -> None:
        """Her ajanı renk kodlu daire olarak çiz, can/enerji barı ekle.

        TODO[Sonnet]: Implement
            for agent in agents:
                if not agent.is_alive: continue
                color = STRATEGY_COLORS.get(agent.strategy_type, (200, 200, 200))
                x_px = agent.y * CELL_SIZE_PX + CELL_SIZE_PX // 2
                y_px = agent.x * CELL_SIZE_PX + CELL_SIZE_PX // 2
                pygame.draw.circle(screen, color, (x_px, y_px), CELL_SIZE_PX // 2 - 2)
                # Health bar üstünde
                bar_w = CELL_SIZE_PX
                health_ratio = agent.health / 100.0
                pygame.draw.rect(screen, (220, 50, 50), (x_px - bar_w//2, y_px - CELL_SIZE_PX, bar_w, 2))
                pygame.draw.rect(screen, (50, 220, 50), (x_px - bar_w//2, y_px - CELL_SIZE_PX, int(bar_w * health_ratio), 2))
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 7'de doldurulacak")

    def _draw_resources(self, resources) -> None:
        """TODO[Sonnet]: Yeşil daireler"""
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 7'de doldurulacak")

    def _draw_obstacles(self, obstacles) -> None:
        """TODO[Sonnet]: Gri kareler"""
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 7'de doldurulacak")

    def _draw_hud(self, env, info: Optional[dict]) -> None:
        """HUD: nesil, adım, hayatta kalan, lider strateji tipi.

        TODO[Sonnet]: Implement
            hud_x = GRID_W * CELL_SIZE_PX + 10
            texts = [
                f"Generation: {info.get('generation', 0)}",
                f"Step: {env.step_count} / {MAX_STEPS}",
                f"Alive: {sum(1 for a in env.agents if a.is_alive)}",
                f"Resources Left: {sum(1 for r in env.resources if not r.consumed)}",
            ]
            for i, text in enumerate(texts):
                surface = self.font.render(text, True, (240, 240, 240))
                self.screen.blit(surface, (hud_x, 20 + i * 24))
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 7'de doldurulacak")

    def save_frame_to_replay(self, frames: list, output_path: str) -> None:
        """Frame'leri MP4'e yaz (sunum yedeği için).

        TODO[Sonnet]: imageio kullan veya cv2.VideoWriter
            import imageio
            imageio.mimsave(output_path, frames, fps=FPS)
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 11'de doldurulacak")

    def close(self) -> None:
        if self._initialized and not self.headless:
            try:
                pygame.quit()
            except Exception:
                pass
