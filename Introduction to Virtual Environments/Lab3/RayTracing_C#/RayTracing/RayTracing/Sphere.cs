using System;

namespace raytracing
{
    /// <summary>
    /// Klasa predstavlja kuglu u prostoru. Nasljeduje apstraktnu klasu Object. Kugla
    /// je odredena svojim polozajem, radijusom, bojom, parametrima materijala i
    /// udjelima pojedninih zraka (osnovne, odbijene i lomljene).
    /// </summary>
    public class Sphere:Object
    {
        private double radius;
        const double Epsilon = 0.0001;
        private Point IntersectionPoint;

        /// <summary>
        /// Inicijalni konstruktor koji postavlja sve parametre kugle. Za prijenos
        /// parametara koristi se pomocna klasa SphereParameters.
        /// </summary>
        /// <param name="sphereParameters">parametri kugle</param>
        public Sphere ( SphereParameters sphereParameters )
            : base(sphereParameters.getCenterPosition(), sphereParameters.getRaysContributions(),
                sphereParameters.getMaterialParameters(), sphereParameters.getN(),
                sphereParameters.getNi())
        {
            this.radius = sphereParameters.getRadius();
        }

        /// <summary>
        /// Metoda ispituje postojanje presjeka zrake ray s kuglom. Ako postoji presjek
        /// postavlja tocku presjeka IntersectionPoint, te
        /// vraca logicku vrijednost true.
        /// </summary>
        /// <param name="ray">zraka za koju se ispituje postojanje presjeka sa kuglom</param>
        /// <returns>logicku vrijednost postojanja presjeka zrake s kuglom</returns>
        public override bool intersection ( Ray ray )
        {
            // chapter 3.3
            // create vector PC
            Vector vectorPC = new Vector(ray.getStartingPoint(), this.getCenterPosition());
            // getAngle method returns value in rad
            double alpha = vectorPC.getAngle(ray.getDirection());
            // alpha value in degrees
            double alphaDegree = (alpha * 180) / Math.PI;
            // check if alpha larger than 90 degrees 
            if (alphaDegree > 90) return false;
            // find distance d from ray to sphere center
            double d = vectorPC.getLength() * Math.Sin(alpha);
            // check if distance is bigger than radius
            if (d > this.radius) return false;
            // distance from vertex P do vertex D
            double pdLength = Math.Sqrt(Math.Pow(vectorPC.getLength(), 2) - Math.Pow(d, 2));
            // find distance from P to closer intersection
            double PcloserIntersection = pdLength - Math.Sqrt(Math.Pow(this.radius, 2) - Math.Pow(d, 2));
            // check if distance is smaller than 0 (with epsilon as a correction factor)
            if (PcloserIntersection  <= 0 + Epsilon)
            {
                PcloserIntersection = pdLength + Math.Sqrt(Math.Pow(this.radius, 2) - Math.Pow(d, 2));
            }
            // using Point class constructor to create an intersection point 
            this.IntersectionPoint = new Point(ray.getStartingPoint(), ray.getDirection(), PcloserIntersection);
            return true;
        }

        /// <summary>
        /// Vraca tocku presjeka kugle sa zrakom koja je bliza pocetnoj tocki zrake.
        /// </summary>
        /// <returns>tocka presjeka zrake s kuglom koja je bliza izvoru zrake</returns>
        public override Point getIntersectionPoint ()
        {
            return IntersectionPoint;
        }

        /// <summary>
        /// Vraca normalu na kugli u tocki point
        /// </summary>
        /// <param name="point">point na kojoj se racuna normala na kugli</param>
        /// <returns>normal vektor normale</returns>
        public override Vector getNormal ( Point point )
        {
            Ray ray = new Ray(this.centerPosition, point);
            Vector normal = ray.getDirection();

            return normal;
        }
    }
}