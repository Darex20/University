using System;

namespace raytracing
{
    /// <summary>
    /// Klasa predstvlja scenu kod modela crtanja slike pomocu ray tracinga. Sastoji
    /// se od izvora svjetlosti i konacnog broja objekata.
    /// </summary>
    public class Scene
    {
        const int MAXDEPTH = 5; //maksimalna dubina rekurzije
        private int numberOfObjects;
        private Sphere[] sphere;
        private Point lightPosition;
        private ColorVector backgroundColors = new ColorVector(0, 0, 0);
        private ColorVector light = new ColorVector((float)1, (float)1, (float)1);
        private ColorVector ambientLight = new ColorVector((float)0.5, (float)0.5, (float)0.5);

        /// <summary>
        /// Inicijalni konstruktor koji postavlja poziciju svijetla i parametre svih
        /// objekata u sceni.
        /// </summary>
        /// <param name="lightPosition">pozicija svijetla</param>
        /// <param name="numberOfObjects">broj objekata u sceni</param>
        /// <param name="sphereParameters">parametri svih kugli</param>
        public Scene ( Point lightPosition, int numberOfObjects, SphereParameters[] sphereParameters )
        {
            this.lightPosition = lightPosition;
            this.numberOfObjects = numberOfObjects;
            sphere = new Sphere[numberOfObjects];
            for(int i = 0; i < numberOfObjects; i++)
            {
                sphere[i] = new Sphere(sphereParameters[i]);
            }
        }

        /// <summary>
        /// Metoda provjerava da li postoji sjena na tocki presjeka. Vraca true ako
        /// se zraka od mjesta presjeka prema izvoru svjetlosti sjece s nekim objektom.
        /// </summary>
        /// <param name="intersection">tocka presjeka</param>
        /// <returns>true ako postoji sjena u tocki presjeka, false ako ne postoji</returns>
        private bool shadow ( Point intersection )
        {
            Ray ray = new Ray(intersection, lightPosition);


            foreach (Sphere s in sphere)
            {
                if (s.intersection(ray)) return true;
            }

            return false;
        }

        /// <summary>
        /// Metoda koja pomocu pracenja zrake racuna boju u tocki presjeka. Racuna se
        /// osvjetljenje u tocki presjeka te se zbraja s doprinosima osvjetljenja koje
        /// donosi reflektirana i refraktirana zraka.
        /// </summary>
        /// <param name="ray">pracena zraka</param>
        /// <param name="depth">dubina rekurzije</param>
        /// <returns>vektor boje u tocki presjeka</returns>
        public ColorVector traceRay(Ray ray, int depth)
        {
            // chapter 3 pseudocode algorithm implementation

            if (depth > MAXDEPTH) return new ColorVector(0, 0, 0);
            double current_distance = 0;
            bool intersection = false;
            Sphere currSphere = null;

            foreach (Sphere s in sphere)
            {
                if(s.intersection(ray) == true)
                {
                    Point intersectionPoint = s.getIntersectionPoint();
                    double distance = ray.getStartingPoint().getDistanceFrom(intersectionPoint);
                    if(!intersection)
                    {
                        current_distance = distance;
                        intersection = true;
                        currSphere = s;
                    } 
                    else if(distance < current_distance)
                    {
                        current_distance = distance;
                        currSphere = s;
                    }
                }
            }
            
            if(!intersection)
            {
                return new ColorVector(backgroundColors.getRed(), backgroundColors.getGreen(), backgroundColors.getBlue());
            }

            PropertyVector ambientCoefficient = currSphere.getKa();
            float ambientLightR = ambientLight.getRed() * ambientCoefficient.getRedParameter();
            float ambientLightG = ambientLight.getGreen() * ambientCoefficient.getGreenParameter();
            float ambientLightB = ambientLight.getBlue() * ambientCoefficient.getBlueParameter();

            ColorVector overallLightComponent = new ColorVector(ambientLightR, ambientLightG, ambientLightB);

            PropertyVector diffuseCoefficient = currSphere.getKd();
            Point closestPoint = currSphere.getIntersectionPoint();

            Vector L = new Vector(closestPoint, lightPosition);
            L.normalize();
            Vector N = currSphere.getNormal(closestPoint);

            float LNdotProduct = (float)L.dotProduct(N);
            if (LNdotProduct > 0 && !shadow(closestPoint))
            {
                float diffuseLightR = light.getRed() * diffuseCoefficient.getRedParameter() * LNdotProduct;
                float diffuseLightG = light.getGreen() * diffuseCoefficient.getGreenParameter() * LNdotProduct;
                float diffuseLightB = light.getBlue() * diffuseCoefficient.getBlueParameter() * LNdotProduct;

                ColorVector diffuseComponent = new ColorVector(diffuseLightR, diffuseLightG, diffuseLightB);
                overallLightComponent = overallLightComponent.add(diffuseComponent);
            }

            
            PropertyVector specularCoefficient = currSphere.getKs();
            Vector R = L.getReflectedVector(N);
            Vector V = new Vector(closestPoint, ray.getStartingPoint());
            R.normalize();
            V.normalize();

            double ni = currSphere.getNi();
            double vn = V.dotProduct(N);
            if (vn < 0)
            {
                N = N.multiple(-1);
                ni = 1.0 / ni;
            }

            double RVproduct = R.dotProduct(V);
            if (RVproduct > 0 && !shadow(closestPoint))
            {
                double specularLightR = light.getRed() * specularCoefficient.getRedParameter() * Math.Pow(RVproduct, currSphere.getN());
                double specularLightG = light.getGreen() * specularCoefficient.getGreenParameter() * Math.Pow(RVproduct, currSphere.getN());
                double specularLightB = light.getBlue() * specularCoefficient.getBlueParameter() * Math.Pow(RVproduct, currSphere.getN());

                ColorVector specularComponent = new ColorVector((float)specularLightR, (float)specularLightG, (float)specularLightB);
                overallLightComponent = overallLightComponent.add(specularComponent);
            }

            Vector reflectedVector = V.getReflectedVector(N);
            reflectedVector.normalize();

            Ray reflectedRay = new Ray(closestPoint, reflectedVector);
            ColorVector colorReflected = traceRay(reflectedRay, depth + 1);

            Vector refractedVector = V.getRefractedVector(N, ni);
            refractedVector.normalize();

            Ray Rrefr = new Ray(closestPoint, refractedVector);
            ColorVector colorRefracted = traceRay(Rrefr, depth + 1);

            overallLightComponent = overallLightComponent.add(colorReflected.multiple(currSphere.getReflectionFactor()));
            overallLightComponent = overallLightComponent.add(colorRefracted.multiple(currSphere.getRefractionFactor()));
            overallLightComponent.correct();

            return overallLightComponent;
        }
    }
}