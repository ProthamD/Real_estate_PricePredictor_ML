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
  FormControl,
  FormLabel,

} from '@chakra-ui/react';
import { WarningIcon, CheckIcon } from '@chakra-ui/icons';

// Import FormControl from the correct package


export default function Home() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const onSubmit = async (data) => {
    try {
      const response = await axios.post('http://localhost:8000/predict', data);
      setPrediction(response.data.predicted_price);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch prediction');
      setPrediction(null);
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
            </FormControl>

            <Button type="submit" colorScheme="blue" width="full" mt={4}>
              Predict Price
            </Button>
          </VStack>
        </form>

        {error && (
          <Alert status="error" mt={4}>
            <WarningIcon mr={2} />
            {error}
          </Alert>
        )}

        {prediction && (
          <Alert status="success" mt={4}>
            <CheckIcon mr={2} />
            Predicted Price: <Text as="b">${prediction}k</Text>
          </Alert>
        )}
      </Box>
    </ChakraProvider>
  );
}