using System;

namespace raytracing
{
    /// <summary>
    /// Klasa predstavlja ekran kroz koji se 'gleda' scena kod modela crtanja slike
    /// pomocu ray tracinga. Ekran je kvadratnog oblika, a definiran je velicinom
    /// stranice i rezolucijom (broj piksela po duzini). Smjesten je u x-y ravninu
    /// tako da mu se centar nalazi u sredistu tog trodimenzionalnog koordinatnog
    /// sustava.
    /// </summary>
    public class Screen
    {
        private double size;
        private int resolution;

        /// <summary>
        /// Glavni konstruktor koji postavlja velicinu i rezoluciju ekrana.
        /// </summary>
        /// <param name="size">velicina stranice ekrana</param>
        /// <param name="resolution">rezolucija ekrana</param>
        public Screen ( double size, int resolution )
        {
            this.size = size;
            this.resolution = resolution;
        }

        /// <summary>
        /// Metoda koja za svaki piksel slike (definiran parom varijabli i,j) vraca
        /// tocku na ekranu.
        /// </summary>
        /// <param name="i">indeks stupca u kojem se nalazi piksel</param>
        /// <param name="j">indeks retka u kojem se nalazi piksel</param>
        /// <returns>koordinate piksela u virtualnom prostoru</returns>
        public Point getPoint ( int i, int j )
        {
            // Chapter 3.1
            // example pixel (-200, 200) returns coordinates (-1, -1, 0)
            double i_double = (double) i;
            double j_double = (double) j;
            double resolution_double = (double) resolution;

            double x = (i_double - resolution_double / 2) / (resolution_double / size);
            double y = (j_double - resolution_double / 2) / (resolution_double / size);

			return new Point(x, y, 0);
        }
    }
}