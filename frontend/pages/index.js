import { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import { 
  ChakraProvider, 
  Box, 
  Heading, 
  Input, 
  Button, 
  VStack, 
  Text, 
  Alert,
  AlertIcon,
  AlertDescription
} from '@chakra-ui/react';
import { 
  FormControl,
  FormLabel,
  FormErrorMessage 
} from '@chakra-ui/form-control';

export default function Home() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data) => {
    setLoading(true);
    setError(null);
    setPrediction(null);
    
    try {
      // Convert all string values to numbers
      const numericData = {};
      for (const key in data) {
        numericData[key] = parseFloat(data[key]);
      }
      
      // Use environment variable for API URL, fallback to localhost for dev
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
      console.log('Making prediction request to:', apiUrl);
      console.log('Data:', numericData);
      
      const response = await axios.post(`${apiUrl}/predict`, numericData);
      
      console.log('Response:', response.data);
      
      // Backend returns { prediction: value, status: "success" }
      setPrediction(response.data.prediction);
      setError(null);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err.response?.data?.error || err.message || 'Failed to fetch prediction');
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Box maxW="md" mx="auto" mt={10} p={5} borderWidth="1px" borderRadius="lg">
        <Heading mb={6} textAlign="center">🏠 Real Estate Price Predictor</Heading>
        
        <form onSubmit={handleSubmit(onSubmit)}>
          <VStack spacing={4}>
            {/* CRIM - Per capita crime rate */}
            <FormControl isInvalid={errors.CRIM}>
              <FormLabel>Crime Rate (CRIM)</FormLabel>
              <Input 
                type="number" 
                step="0.00001"
                {...register("CRIM", { 
                  required: "Required",
                  min: { value: 0, message: "Must be positive" }
                })} 
              />
              <FormErrorMessage>
                {errors.CRIM && errors.CRIM.message}
              </FormErrorMessage>
            </FormControl>

            {/* ZN - Residential land proportion */}
            <FormControl isInvalid={errors.ZN}>
              <FormLabel>Residential Land (ZN)</FormLabel>
              <Input 
                type="number" 
                step="1"
                {...register("ZN", { 
                  required: "Required",
                  min: { value: 0, message: "Must be positive" }
                })} 
              />
              <FormErrorMessage>
                {errors.ZN && errors.ZN.message}
              </FormErrorMessage>
            </FormControl>

            {/* INDUS - Non-retail business acres */}
            <FormControl isInvalid={errors.INDUS}>
              <FormLabel>Non-Retail Business (INDUS)</FormLabel>
              <Input 
                type="number" 
                step="0.01"
                {...register("INDUS", { 
                  required: "Required",
                  min: { value: 0, message: "Must be positive" }
                })} 
              />
              <FormErrorMessage>
                {errors.INDUS && errors.INDUS.message}
              </FormErrorMessage>
            </FormControl>

            {/* CHAS - Charles River dummy */}
            <FormControl isInvalid={errors.CHAS}>
              <FormLabel>Charles River (CHAS: 0 or 1)</FormLabel>
              <Input 
                type="number" 
                min="0"
                max="1"
                {...register("CHAS", { 
                  required: "Required",
                  validate: value => [0, 1].includes(Number(value)) || "Must be 0 or 1"
                })} 
              />
              <FormErrorMessage>
                {errors.CHAS && errors.CHAS.message}
              </FormErrorMessage>
            </FormControl>

            {/* NOX - Nitric oxides concentration */}
            <FormControl isInvalid={errors.NOX}>
              <FormLabel>Nitric Oxides (NOX)</FormLabel>
              <Input 
                type="number" 
                step="0.0001"
                {...register("NOX", { 
                  required: "Required",
                  min: { value: 0, message: "Must be positive" }
                })} 
              />
              <FormErrorMessage>
                {errors.NOX && errors.NOX.message}
              </FormErrorMessage>
            </FormControl>

            {/* RM - Average rooms */}
            <FormControl isInvalid={errors.RM}>
              <FormLabel>Avg Rooms (RM)</FormLabel>
              <Input 
                type="number" 
                step="0.1"
                {...register("RM", { 
                  required: "Required",
                  min: { value: 3, message: "Minimum 3 rooms" }
                })} 
              />
              <FormErrorMessage>
                {errors.RM && errors.RM.message}
              </FormErrorMessage>
            </FormControl>

            {/* AGE - Owner-occupied units */}
            <FormControl isInvalid={errors.AGE}>
              <FormLabel>Owner-Occupied Units (AGE)</FormLabel>
              <Input 
                type="number" 
                step="0.1"
                {...register("AGE", { 
                  required: "Required",
                  min: { value: 0, message: "Must be positive" }
                })} 
              />
              <FormErrorMessage>
                {errors.AGE && errors.AGE.message}
              </FormErrorMessage>
            </FormControl>

            {/* DIS - Employment center distance */}
            <FormControl isInvalid={errors.DIS}>
              <FormLabel>Employment Center Distance (DIS)</FormLabel>
              <Input 
                type="number" 
                step="0.0001"
                {...register("DIS", { 
                  required: "Required",
                  min: { value: 0, message: "Must be positive" }
                })} 
              />
              <FormErrorMessage>
                {errors.DIS && errors.DIS.message}
              </FormErrorMessage>
            </FormControl>

            {/* RAD - Highway accessibility */}
            <FormControl isInvalid={errors.RAD}>
              <FormLabel>Highway Accessibility (RAD)</FormLabel>
              <Input 
                type="number" 
                step="1"
                {...register("RAD", { 
                  required: "Required",
                  min: { value: 1, message: "Minimum 1" }
                })} 
              />
              <FormErrorMessage>
                {errors.RAD && errors.RAD.message}
              </FormErrorMessage>
            </FormControl>

            {/* TAX - Property tax rate */}
            <FormControl isInvalid={errors.TAX}>
              <FormLabel>Property Tax (TAX)</FormLabel>
              <Input 
                type="number" 
                step="1"
                {...register("TAX", { 
                  required: "Required",
                  min: { value: 100, message: "Minimum $100" }
                })} 
              />
              <FormErrorMessage>
                {errors.TAX && errors.TAX.message}
              </FormErrorMessage>
            </FormControl>

            {/* PTRATIO - Pupil-teacher ratio */}
            <FormControl isInvalid={errors.PTRATIO}>
              <FormLabel>Pupil-Teacher Ratio (PTRATIO)</FormLabel>
              <Input 
                type="number" 
                step="0.1"
                {...register("PTRATIO", { 
                  required: "Required",
                  min: { value: 10, message: "Minimum 10:1" }
                })} 
              />
              <FormErrorMessage>
                {errors.PTRATIO && errors.PTRATIO.message}
              </FormErrorMessage>
            </FormControl>

            {/* B - Black population proportion */}
            <FormControl isInvalid={errors.B}>
              <FormLabel>Black Population (B)</FormLabel>
              <Input 
                type="number" 
                step="0.1"
                {...register("B", { 
                  required: "Required",
                  min: { value: 0, message: "Must be positive" }
                })} 
              />
              <FormErrorMessage>
                {errors.B && errors.B.message}
              </FormErrorMessage>
            </FormControl>

            {/* LSTAT - Lower status population */}
            <FormControl isInvalid={errors.LSTAT}>
              <FormLabel>Lower Status Population (LSTAT)</FormLabel>
              <Input 
                type="number" 
                step="0.01"
                {...register("LSTAT", { 
                  required: "Required",
                  min: { value: 0, message: "Must be positive" }
                })} 
              />
              <FormErrorMessage>
                {errors.LSTAT && errors.LSTAT.message}
              </FormErrorMessage>
            </FormControl>

            <Button 
              type="submit" 
              colorScheme="blue" 
              width="full" 
              mt={4}
              isLoading={loading}
              loadingText="Predicting..."
            >
              Predict Price
            </Button>
          </VStack>
        </form>

        {error && (
          <Alert status="error" mt={4}>
            <AlertIcon />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {prediction && (
          <Alert status="success" mt={4}>
            <AlertIcon />
            <AlertDescription>
              Predicted Price: <Text as="b">${prediction}k</Text>
            </AlertDescription>
          </Alert>
        )}
      </Box>
    </ChakraProvider>
  );
}